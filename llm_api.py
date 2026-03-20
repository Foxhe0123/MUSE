import openai
# from api import SearchAPI, paragraph_to_image, InnerSearchAPI
import json

import prompts
from base import callLLM, read_from_txt
# , callGPT
import re
from logger_config import get_logger

# Get the configured logger
logger = get_logger()

def Analyze(theme, text, previous="", isFeedback = True, feedback_file = 'writting_suggestions.txt'):
    query =prompts.LLM_api_Analyze_Write_PROMPT
    if isFeedback:
        logger.info("isFeedback:"+str(isFeedback))
        suggestions = read_from_txt(feedback_file)
    else:
        suggestions = [
            '1. Use transition sentences between paragraphs to help readers understand the connection between the previous and next content.',
            '2. Use conjunctions appropriately to make the article more fluent.']
    query = query.format(theme=theme, previous=previous, text=text, suggestions=suggestions)
    logger.info("Writing Prompt:"+query)
    response = callLLM(query=query)
    logger.info("Writing Response:" + response)
    return response


def Search(query):
    prompt = prompts.LLM_api_Search_PROMPT
    prompt = prompt.format(query=query)
    logger.info("Search Prompt:"+prompt)
    search_query = callLLM(prompt)
    logger.info("Search Response:" + search_query)
    # search_query = ""
    # while search_query != "":
    #     try:
    #         search_query = callLLM(prompt)
    #     except:
    #         pass
    result = json.loads(search_query[8:-4])['parameters']['query']
    # result = ""
    # while result != "":
    #     try:
    #         result = json.loads(search_query[8:-4])['arguments']['query']
    #     except:
    #         pass
    # search_query = re.split(" |，", search_query)
    # search_query[-1] = '"' + search_query[-1] + '"'
    # search_query = " ".join(search_query)
    return result

def PosterImg(query):
    prompt = prompts.LLM_api_PosterImg_PROMPT
    prompt = prompt.format(query=query)
    t2i_query = callLLM(prompt)
    t2i_query = json.loads(t2i_query[8:-4])
    logger.notice(t2i_query)
    return paragraph_to_image(t2i_query['arguments']['description'])['img_url']


def Text2Img(query):
    prompt = prompts.LLM_api_Text2Img_PROMPT
    prompt = prompt.format(query=query)
    t2i_query = callLLM(prompt)
    t2i_query = json.loads(t2i_query[8:-4])
    return paragraph_to_image(t2i_query['arguments']['query'])['img_url']


def Select_Search_or_Generation(caption):
    prompt = prompts.LLM_api_Select_Search_or_Generation_PROMPT
    prompt = prompt.format(caption=caption)
    res = callLLM(prompt)
    if "生成" in res[:2]:
        return 0
    elif "搜索" in res[:2]:
        return 1
    else:
        return -1


def Summary(text):
    prompt = prompts.LLM_api_Summary_PROMPT
    prompt = prompt.format(text=text)
    logger.info("Summary Prompt:" + prompt)
    response = callLLM(prompt)
    logger.info("Summary Response:" + response)
    return response


def Title(outline):
    prompt = prompts.LLM_api_Title_PROMPT
    prompt = prompt.format(outline=outline)
    logger.info("Title Prompt:" + prompt)
    response = callLLM(prompt)
    logger.info("Title Response:" + response)
    return response

def callExtract(query):
    prompt = prompts.LLM_api_callExtract_PROMPT
    prompt = prompt.format(query=query)
    logger.info("callExtract Prompt:" + prompt)
    response = callLLM(prompt)
    logger.info("callExtract Response:" + response)
    return response

def InsertImg(outline):
    prompt = prompts.LLM_api_InsertImg_PROMPT
    prompt = prompt.format(outline=outline)
    return callLLM(prompt)
    # return callGPT(prompt)

