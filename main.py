from base import set_model
from llm_api import Analyze, Search, Text2Img, Select_Search_or_Generation, Summary, Title, InsertImg, PosterImg
from api import SearchAPI, cos_sim, google_search_img, get_text_sim
from structure import Outline, Outline_new
import markdown
import json
import argparse
import os
import re

from transition_group import Add_transition
from logger_config import get_logger
from writer_group import Write

# Get the configured logger
logger = get_logger()


def safeFilename(filename, replace=''):
    return re.sub(re.compile(
        '[/\\:*?"<>|]')
        , replace,
        filename
    )



def GetImg(caption):
    logger.notice(f"{caption} in the illustration...")
    if True: # 1 means search
        url = google_search_img(caption)
    else: # 0 means generate
        url = Text2Img(caption)
    return url

def Merge_paragraph(outline, content):
    output = ""
    output_without_outline = ""
    outlines = outline.split('\n')
    for paragraph in outline.split('\n'):
        if paragraph == '':
            continue
        if paragraph.startswith("Image_caption"):
            caption = paragraph.split("Image_caption[")[1][:-1]
            img_url = GetImg(caption)
            output += f"![image]({img_url})" + '\n'
            output_without_outline += f"![image]({img_url})" + '\n'
        else:
            output += paragraph + '\n'
            if paragraph in content.keys():
                if content[paragraph] != []:
                    if "Output:\n" in content[paragraph][0]:
                        content[paragraph][0] = content[paragraph][0].split("Output:\n", 1)[-1]
                    for line in content[paragraph]:
                        output += '\n&ensp;&ensp;&ensp;&ensp;' + line + '\n'
                        output_without_outline += '\n&ensp;&ensp;&ensp;&ensp;' + line + '\n'
    return output, output_without_outline

def Generate_all(task,edit_epic, isRead, isEdit, isFeedback,model):

    logger.notice('The task：'+task)
    logger.notice('Generating outline...')
    # outline = Structure(task)  # Direct Generation
    #outline = Outline(task)  # ReAct framework generation
    outline = Outline_new(task)
    outline = re.sub('[ ]{2,}', '', outline)

    logger.notice('Start writing...')
    content, summary = Write(task, outline,edit_epic, isRead, isEdit, isFeedback)

    # Merge article without Modify
    output_without_Modify, output_nooutline_withoutModify = Merge_paragraph(outline, content)

    logger.notice('Overall modification...')
    content = Add_transition(outline, content)
    output,output_without_outline = Merge_paragraph(outline, content)

    logger.notice('Generating title...')
    title = Title(outline)
    title = safeFilename(title)
    logger.notice("Title："+title)
    output_without_Modify = f"#  <center> {title}\n" + output_without_Modify
    output = f"#  <center> {title}\n" + output
    output_without_outline = f"#  <center> {title}\n" + output_without_outline
    os.makedirs('./output', exist_ok=True)
    #output article without Modify
    title = title +"("+model+")"
    if not isEdit:
        title = title + "(without Edit)"
    elif not isRead:
        title = title + "(without Read)"
    with open(f"output/{title}(without_Modify).md", 'w', encoding='utf-8') as f:
        f.write(output_without_Modify)
    #output
    with open(f"output/{title}.md", 'w', encoding='utf-8') as f:
        f.write(output)
    with open(f"output/{title}(without_outline).md", 'w', encoding='utf-8') as f:
        f.write(output_without_outline)
    html_output = markdown.markdown(output)
    with open(f"output/{title}.html", 'w', encoding='utf-8') as f:
        f.write(html_output)
    html_output_without_outline = markdown.markdown(output_without_outline)
    with open(f"output/{title}(without_outline).html", 'w', encoding='utf-8') as f:
        f.write(html_output_without_outline)
    logger.notice('Complete the creation')
    return


def Generate_withoutline(task,edit_epic, isRead, isEdit, isFeedback,model):

    logger.notice('The task：'+task)
    logger.notice('Read outline...')
    # outline = Structure(task)  # Direct Generation
    #outline = Outline(task)  # ReAct framework generation
    #outline = Outline_new(task)
    # 读取文件并处理
    with open('outline.txt', 'r', encoding='utf-8') as f:
        # 读取所有非空行，并去掉末尾空格
        lines = [line.rstrip() for line in f if line.strip()]

    outline = '\n'.join(lines) + '\n'

    outline = re.sub(r'[ ]{2,}', '', outline)
    #outline = re.sub('[ ]{2,}', '', outline)
    logger.notice(outline)

    logger.notice('Start writing...')
    content, summary = Write(task, outline,edit_epic, isRead, isEdit, isFeedback)

    # Merge article without Modify
    output_without_Modify, output_nooutline_withoutModify = Merge_paragraph(outline, content)

    logger.notice('Overall modification...')
    content = Add_transition(outline, content)
    output,output_without_outline = Merge_paragraph(outline, content)

    logger.notice('Generating title...')
    title = Title(outline)
    title = safeFilename(title)
    logger.notice("Title："+title)
    output_without_Modify = f"#  <center> {title}\n" + output_without_Modify
    output = f"#  <center> {title}\n" + output
    output_without_outline = f"#  <center> {title}\n" + output_without_outline
    os.makedirs('./output', exist_ok=True)
    #output article without Modify
    title = title +"("+model+")"
    if not isEdit:
        title = title + "(without Edit)"
    elif not isRead:
        title = title + "(without Read)"
    with open(f"output/{title}(without_Modify).md", 'w', encoding='utf-8') as f:
        f.write(output_without_Modify)
    #output
    with open(f"output/{title}.md", 'w', encoding='utf-8') as f:
        f.write(output)
    with open(f"output/{title}(without_outline).md", 'w', encoding='utf-8') as f:
        f.write(output_without_outline)
    html_output = markdown.markdown(output)
    with open(f"output/{title}.html", 'w', encoding='utf-8') as f:
        f.write(html_output)
    html_output_without_outline = markdown.markdown(output_without_outline)
    with open(f"output/{title}(without_outline).html", 'w', encoding='utf-8') as f:
        f.write(html_output_without_outline)
    logger.notice('Complete the creation')
    return


if __name__ == "__main__":
    # Initialize argument parser
    parser = argparse.ArgumentParser(description='YNKN generation framework')

    # Task description (e.g., article topic)
    #task = "Write an article introducing Inception"
    #task = "Write a novel about young people's love on campus"
    #task= "Write an article introducing Sydney Opera House"
    task = "Write an article introducing Hemingway's Novel The Old Man and the Sea"
    parser.add_argument('--task', type=str, default=task, help='The article writing task description.')

    # Model name, e.g., deepseek, gpt-4, gpt-3.5-turbo, etc.
    parser.add_argument('--model', type=str, default="gpt-4o-mini", help='Name of the LLM model to use.')

    # Whether to enable editing module
    # If isEdit is False, Read and Feedback modules will be automatically disabled
    parser.add_argument('--isEdit', type=bool, default=True, help='Enable editing module (True/False).')

    # Number of editing iterations (only effective if isEdit=True)
    parser.add_argument('--edit_epic', type=int, default=1, help='Number of editing iterations.')

    # Whether to enable the reading group to raise issues
    parser.add_argument('--isRead', type=bool, default=True, help='Enable reading group for question generation.')

    # Whether to enable feedback-based editing refinement
    parser.add_argument('--isFeedback', type=bool, default=True, help='Enable feedback module for improvement.')

    # Parse arguments
    args = parser.parse_args()

    # Initialize model using configuration
    set_model(args.model)

    # Start the full article generation process
    #Generate_all(args.task,args.edit_epic, args.isRead, args.isEdit, args.isFeedback,args.model)
    Generate_withoutline(args.task, args.edit_epic, args.isRead, args.isEdit, args.isFeedback, args.model)