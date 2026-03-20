from api import SearchAPI, get_text_sim
from editor_group import edit, edit_only, structure_edit
from llm_api import Search, Analyze, Summary
from logger_config import get_logger
import spacy
from reader_group import readers, readers_concurrency

# Get the configured logger
logger = get_logger()

def stopwordslist(path):
    stopwords = [line.strip() for line in open(path, encoding='UTF-8').readlines()]
    return stopwords

def get_keywords(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    keyword_phrases = []
    for chunk in doc.noun_chunks:
        keyword_phrases.append(chunk.text)
    return keyword_phrases


def write_read_edit(task, title, text, edit_epic, isRead, isFeedback):
    # read section and get the feedback
    n = 0
    while n < edit_epic:
        logger.notice('开始第'+str(n+1)+'/'+str(edit_epic)+'轮修改')
        if isRead:
            logger.info("isRead:" + str(isRead))
            # review = read(text)
            # reviews = readers(task,title,text)
            reviews = readers_concurrency(task, title, text)
            review = "\n".join(reviews)
            logger.notice("--------review:")
            logger.notice(review)
            new_article, suggestions = edit(text, review, isFeedback)

        else:
            logger.info("isRead:" + str(isRead))
            new_article, suggestions = edit_only(text, isFeedback)
        new_article = structure_edit(new_article)
        logger.notice("--------article:")
        logger.notice(new_article)
        logger.notice("--------suggestions:")
        logger.notice(suggestions)
        text = new_article
        n+=1
    return text

def Write(task, outline,edit_epic, isRead, isEdit, isFeedback):
    stopwords = stopwordslist('./baidu_stopwords.txt')
    content = {} # List to store generated content
    history_summary = [] # Summary of historical generated content
    outline = outline.strip().split('\n')
    for i in range(len(outline)):
        section = outline[i]
        content[section] = []
        prev_text = ""
        if section == '':
            continue
        if section.split()[0] == "###":
            current_section = " ".join(section.split()[2:])
            logger.notice(f"{current_section} Writing...")
            theme = '\n'.join([task, parent_section, current_section])
        elif section.split()[0] == "##":
            parent_section = " ".join(section.split()[2:])
            if (i == len(outline) - 1 or outline[i + 1].split()[0] == "##"):
                logger.notice(f"{parent_section} Writing...")
                theme = '\n'.join([task, parent_section])
            else:
                edit_sign = True
                continue
        # if section.split()[0] != "###":
        #     continue
        # current_section = section.split()[-1]

        # theme = '\n'.join([task, parent_section, current_section])
        search_keyword = Search(task).split(',')
        # concept = list(spacy.load("en_core_web_sm")(parent_section))
        concept = get_keywords(parent_section)
        new_concept = []
        for c_i in range(len(concept)):
            if len(concept[c_i]) < 2 or concept[c_i] in stopwords:
                continue
            tag = True
            for c_j in range(c_i + 1, len(concept)):
                if concept[c_i] in concept[c_j]:
                    tag = False
                    break
            if tag:
                new_concept.append(concept[c_i])
        end_idx = 2
        while end_idx <= len(new_concept):
            tmp_message = ""
            end_idx += 2
            tmp_search_keywords = search_keyword + new_concept[:2] + new_concept[end_idx - 2: end_idx]
            tmp_search_keywords.sort(key=lambda x: len(x))
            new_search_keywords = []
            for s_i in range(len(tmp_search_keywords)):
                tag = True
                for s_j in range(s_i + 1, len(tmp_search_keywords)):
                    if tmp_search_keywords[s_i] in tmp_search_keywords[s_j]:
                        tag = False
                        break
                if tag:
                    new_search_keywords.append(tmp_search_keywords[s_i])
            search_message = SearchAPI(" ".join(list(set(new_search_keywords))))
            while len(tmp_message) < 50 or "sorry" in tmp_message:
                tmp_message = Analyze(theme, search_message, "".join(history_summary[-4:]), isFeedback)
                if search_message == "":
                    tmp_message = ".".join(tmp_message.split(".")[1:])
                tmp_message_lists = tmp_message.split("\n\n")
                logger.info("\n".join(tmp_message_lists))
                processed_tmp_message = [tm if tm[-1] == "." else "" for tm in tmp_message_lists]
                tmp_message = "".join(processed_tmp_message)
            if content[section] == [] or get_text_sim(tmp_message, content[section]) < 0.85:
                tmp_summary = Summary(tmp_message)
                if content[section] == []:
                    content[section].append(tmp_message)
                else:
                    tmp_message = ".".join(tmp_message.split(".")[1:])
                    content[section].append(tmp_message)
                prev_text = tmp_message
                history_summary.append(tmp_summary)
        logger.notice('content[' + " ".join(section.split()[2:]) + ']:')
        logger.notice(content[section])
        if isEdit:
            logger.info("isEdit:" + str(isEdit))
            content[section] = write_read_edit(task, section, content[section], edit_epic, isRead, isFeedback)
            logger.notice('new_content[' + " ".join(section.split()[2:]) + ']:')
            logger.notice(content[section])
    return content, history_summary
