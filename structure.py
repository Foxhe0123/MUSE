import openai
import os

import prompts
# from llm_api import Search
from api import SearchAPI, search_content
import json
import requests
from base import callLLM, split_into_list
from llm_api import Search
from logger_config import get_logger
import re

# Get the configured logger
logger = get_logger()

def callgpt4(query):
    result = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": query}])
    message = result['choices'][0]['message']['content']
    # logger.notice(message)
    return message

def Add(outline, theme):
    query = prompts.Outline_Add_PROMPT
    query = query.format(outline=outline, theme=theme)
    logger.info("Outline Add Prompt:" + query)
    # message = callgpt4(query=query)
    message = callLLM(query=query)
    logger.info("Outline Add Response:" + message)

    # info = json.dumps({"prompt":query,"completion":message}, ensure_ascii=False)
    # with open('Add.txt','a') as f:
    #     f.write(info + '\n')

    return message


def SearchQA(query):
    search_result = SearchAPI(query)
    logger.notice(f"SearchResult:\n{search_result}")
    prompt = prompts.Outline_SearchQA_PROMPT

    query = prompt.format(search_result=search_result[:1500], query=query)
    logger.info("Outline SearchQA Prompt:" + query)
    message = callLLM(query)
    logger.info("Outline SearchQA Response:" + message)
    return message

def Outline(keywords):
    system_intel = prompts.Outline_PROMPT

    outline = ""
    history = "\n"
    i = 0

    loop = True
    while loop==True:
        # if query == '':
        #     loop = False
        #     break
        #query = system_intel.format(history=history, query=keywords)
        query = system_intel.format(history=history, query=keywords)
        logger.info("Outline Prompt:" + query)
        message = callLLM(query)
        logger.notice(message)
        history += message + "\n\n"
        api_calls = [line.strip() for line in message.split('\n') if line.startswith('Act')]
        for api_call in api_calls:
            api_input = api_call.split('[')[-1].split(']')[0]
            i += 1
            if 'Finish' in api_call:
                outline = Add(outline, api_input)
                logger.notice(f"Obs {i}:\n" + outline + '\n')
                # query += message + f"\nObs {i}:\n" + outline + '\n'
                # query += f"\nObs {i}:\n" + outline + '\n'
                loop = False
                break
            elif 'Search' in api_call:
                # search_keyword = Search(query).split(',')[:-1]
                search_keyword = Search(api_input)
                # result = SearchQA(api_input + " ".join(search_keyword))
                result = SearchQA(search_keyword)
                logger.notice(f"Obs {i}:\n" + result + '\n')
                # query += message + f"\nObs {i}:\n" + result + '\n'
                # query += f"\nObs {i}:\n" + result + '\n'
            elif 'Add' in api_call:
                outline = Add(outline, api_input)
                logger.notice(f"Obs {i}:\n" + outline + '\n')
                # query += message + f"\nObs {i}:\n" + outline + '\n'
                # query += f"\nObs {i}:\n" + outline + '\n'

    return outline

def Outline_new(keywords):
    reference = search_content(keywords)
    reference_text = ''
    for key, value in reference.items():
        reference_text += key + '\n' + value + '\n\n'
    topic_prompt = prompts.Outline_Topic_PROMPT.format(task=keywords, reference=reference_text)
    logger.info("Outline Topic Prompt:" + topic_prompt)
    topics = callLLM(topic_prompt)
    logger.notice("Outline Topic:" + topics)

    draft_prompt = prompts.Outline_Select_Topic_PROMPT.format(task=keywords, topics=topics)
    logger.info("Outline draft Prompt:" + draft_prompt)
    draft = callLLM(draft_prompt)
    logger.info("Outline draft:" + draft)

    chapter_outline = split_into_list(draft)
    outline_list = {}
    for i in range(len(chapter_outline)):
        chapter_title = re.sub(r'\d+\.\s*', '', chapter_outline[i])
        sub_outline_prompt = prompts.Outline_Sub_outline_PROMPT.format(title=chapter_title, outline=chapter_outline)
        logger.info("sub outline Prompt:" + sub_outline_prompt)
        sub_outline = callLLM(sub_outline_prompt)
        logger.info("sub outline:\n" +"chapter:"+ chapter_title+"\n"+sub_outline)
        if sub_outline == "[none]":
            outline_list[chapter_title] = []
        else:
            sub_titles = split_into_list(sub_outline)
            outline_list[chapter_title] = sub_titles
    outline_str = []
    for index, (key, values) in enumerate(outline_list.items(), start=1):
        # 添加主标题
        outline_str.append(f"## {index}. {key}")
        # 添加子标题
        for sub_index, value in enumerate(values, start=1):
            sub_title = re.sub(r'\d+(\.\d+)*\.\s*', '', value)
            outline_str.append(f"### {index}.{sub_index}. {sub_title}")
    outline =  '\n'.join(outline_str)
    logger.notice("Outline:\n" + outline)
    return outline


if __name__ == "__main__":
    # message = Outline("Help me write a copy introducing Apple.")
    #message = Outline("Help me write a popular science article introducing reinforcement learning.")

    result = Outline_new("Write an article introducing 'Interstellar'")
    print(result)
    # with open('test.md','w') as f:
    #     f.write(message)