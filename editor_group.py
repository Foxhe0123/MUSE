# import json
#
# from click import prompt
import prompts
from base import callLLM,clean_text,clean_text_symbol,save_to_txt,read_from_txt
from logger_config import get_logger

# Get the configured logger
logger = get_logger()
# Editor Group. Some agents for editing articles. Responsible for editing articles based on revision feedback, analyzing feedback, and outputting revised articles and writing suggestions

def edit(article, review, isFeedback):
    suggestion = []
    new_article = []
    while not suggestion or suggestion == "null":
        prompt = prompts.Editor_edit_PROMPT
        prompt = prompt.format(article=article, review=review)
        logger.info("Editor Prompt:" + prompt)
        result = callLLM(prompt)
        logger.info("Editor Response:" + result)
        new_article, suggestion = parse_result_to_dict(result)
    if isFeedback:
        save_feedback(suggestion)
    return new_article,suggestion

def edit_only(article, isFeedback):
    suggestion = []
    new_article = []
    while not suggestion or suggestion == "null":
        prompt = prompts.Editor_only_edit_PROMPT
        prompt = prompt.format(article=article)
        logger.info("only_Editor Prompt:" + prompt)
        result = callLLM(prompt)
        logger.info("only_Editor Response:" + result)
        new_article, suggestion = parse_result_to_dict(result)
    if isFeedback:
        save_feedback(suggestion)
    return new_article,suggestion

def parse_result_to_dict(result):
    # Split the text by keywords "Article" and "Suggestions"
    result = clean_text_symbol(result)
    sections = result.split("Suggestions:")
    new_article = sections[0].replace("Article:", "").strip().split("\n\n")

    # Extract suggestions and put them in a list
    if len(sections)<2:
        suggestion_list = []
        logger.warning("suggestions is null")
    else:
        suggestion_list = sections[1].strip().split("\n")
    # suggestions = [p.split('. ', 1)[1] for p in suggestion_list if p]

    return new_article, suggestion_list

def save_feedback(new_suggestions, feedback_file = 'writting_suggestions.txt'):
    old_suggestions = read_from_txt(feedback_file)
    prompt = prompts.Editor_feedback_PROMPT
    prompt = prompt.format(old_suggestions=old_suggestions, new_suggestions=new_suggestions)
    logger.info("Editor feedback Prompt:" + prompt)
    suggestions = callLLM(prompt)
    logger.info("Editor feedback Response:" + suggestions)
    save_to_txt(feedback_file, suggestions)

#Additional structural modifications
def structure_edit(article):
    prompt = prompts.Editor_structure_edit_PROMPT.format(article=article)
    logger.info("structure_edit Prompt:" + prompt)
    new_article = callLLM(prompt)
    logger.info("structure_edit Response:" + new_article)
    return new_article.strip().split("\n\n")

if __name__ == "__main__":
    # Input text
    text = """The Great Wall, one of the most iconic symbols of China, stands as a testament to the country's rich history and cultural heritage. Stretching over 13,000 miles, it is not just a physical barrier but also a monumental achievement in engineering and defense. Constructed over several dynasties, the Great Wall has evolved from its initial purpose as a military fortification to become a symbol of national pride and unity. Its strategic location along the northern borders of China reflects the ancient Chinese philosophy of defense and protection. The wall's construction involved millions of laborers, showcasing the immense human effort and dedication that went into its creation. Today, the Great Wall attracts millions of tourists annually, who come to marvel at its grandeur and learn about its historical significance. Beyond its physical presence, the Great Wall has also left an indelible mark on Chinese culture, appearing in literature, art, and folklore. It is a living museum that tells the story of China's past while continuing to inspire future generations with its enduring legacy."""
    review = """Reviews: 
The article provides a comprehensive overview of the Great Wall, highlighting its historical significance, cultural impact, and modern-day relevance. However, there are several areas where the writing could be improved for clarity, flow, and engagement.

Problems: 
1. Lack of Transitional Sentences: The article shifts abruptly between different aspects of the Great Wall without smooth transitions. For example, moving from its physical construction to its cultural impact feels disjointed.
2. Overuse of Passive Voice: The text contains several instances where passive voice is used excessively, making the writing less engaging. For example, "The wall's construction involved millions of laborers" could be rephrased to "Millions of laborers were involved in the wall's construction."
3. Lack of Specific Examples: While the article mentions that the Great Wall appears in literature, art, and folklore, it does not provide specific examples or details to illustrate these points.
4. Inconsistent Tone: The tone shifts between formal and informal language throughout the article. For instance, "who come to marvel at its grandeur" is more informal compared to other parts of the text.
5. Overuse of Complex Sentences: Some sentences are overly complex with multiple clauses, which can make them difficult to follow. For example, "Its strategic location along the northern borders of China reflects the ancient Chinese philosophy of defense and protection." could be simplified for better readability.
"""

    new_article, suggestions= edit(text, review)
    logger.notice("--------article:")
    logger.notice(new_article)
    logger.notice("--------suggestions:")
    logger.notice(suggestions)
    # Convert text to dictionary

