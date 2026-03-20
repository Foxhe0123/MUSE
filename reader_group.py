import json
import re

from click import prompt
from concurrent.futures import ThreadPoolExecutor

import prompts
from base import callLLM
from logger_config import get_logger

# Get the configured logger
logger = get_logger()

# Read Group  Some agents for reading articles. Responsible for reading articles, understanding article content, identifying article problems, and providing feedback.

def read(article):
    prompt = prompts.Reader_read_PROMPT
    prompt = prompt.format(article=article)
    logger.info("reader Prompt:" + prompt)
    response = callLLM(prompt)
    logger.info("reader Response:" + response)
    return response

#Create readers with different reading perspectives
def read_org(task, title):
    prompt = prompts.Reader_read_org_PROMPT
    prompt = prompt.format(task=task, title=title)
    logger.info("reader_org Prompt:" + prompt)
    readers = callLLM(prompt)
    logger.info("reader_org Response:" + readers)

    logger.notice(readers)
    reader_list,reader_dir = get_reader_list(readers)
    return reader_list,reader_dir

def create_reader(reader, reader_list, read_des, task):
    prompt = prompts.Reader_create_reader_PROMPT
    prompt = prompt.format(reader=reader, read_des=read_des, readers=reader_list, task=task)
    logger.info("Create reader Prompt:" + prompt)
    readers = callLLM(prompt)
    logger.info("Create reader Response:" + readers)
    reader_prompt = readers+ prompts.Reader_create_reader_output_PROMPT
    return reader_prompt

# Convert the result into a dictionary
def parse_review_to_dict(review):
    # Split the text by keywords "Article Review" and "Article Problems"
    sections = review.split("Problems:")
    article_review = sections[0].replace("Reviews:", "").strip()

    # Extract problems and put them in a list
    problems_list = sections[1].strip().split("\n")
    problems = [p.split('. ', 1)[1] for p in problems_list if p]

    # Construct the dictionary
    review_dict = {
        "review": article_review,
        "problems": problems
    }
    return review_dict

# Convert the reader to a list
def get_reader_list(reader):
    reader_list = []
    reader_dir = {}
    sections = reader.split("\n")
    i = 1
    for section in sections:
        if section.strip().startswith("perspective"+str(i)+":"):
            reader_list.append(section.replace("perspective"+str(i)+":", "").replace("*", "").strip())
            i += 1
        else:
            if reader_list[i-2] in reader_dir:
                reader_dir[reader_list[i - 2]] += section
            else:
                reader_dir[reader_list[i-2]] = section
    return reader_list,reader_dir


#reader module entry
def readers(task, title, article):
    reader_list, reader_dir = read_org(task, title)
    reviews = []
    for reader in reader_list:
        read_prompt = create_reader(reader, reader_list, reader_dir[reader], task)
        prompt = read_prompt.format(article=article)
        logger.info("reader Prompt:" + prompt)
        review = callLLM(prompt)
        logger.info("reader Response:" + review)
        reviews.append(review)
    return reviews

#Concurrent reader entry
def readers_concurrency(task, title, article):
    reader_list, reader_dir = read_org(task, title)
    reviews = []

    def process_reader(reader):
        """
     Processes tasks for a single reader.
        """
        read_prompt = create_reader(reader, reader_list, reader_dir[reader], task)
        prompt = read_prompt.format(article=article)
        logger.info("reader Prompt:" + prompt)
        review = callLLM(prompt)
        logger.info("reader Response:" + review)
        return review

    # Use thread pool for concurrent execution

    with ThreadPoolExecutor(max_workers = 6) as executor:
        reviews = list(executor.map(process_reader, reader_list))

    return reviews



if __name__ == "__main__":
    # Input text
    # text = """The Great Wall, one of the most iconic symbols of China, stands as a testament to the country's rich history and cultural heritage. Stretching over 13,000 miles, it is not just a physical barrier but also a monumental achievement in engineering and defense. Constructed over several dynasties, the Great Wall has evolved from its initial purpose as a military fortification to become a symbol of national pride and unity. Its strategic location along the northern borders of China reflects the ancient Chinese philosophy of defense and protection. The wall's construction involved millions of laborers, showcasing the immense human effort and dedication that went into its creation. Today, the Great Wall attracts millions of tourists annually, who come to marvel at its grandeur and learn about its historical significance. Beyond its physical presence, the Great Wall has also left an indelible mark on Chinese culture, appearing in literature, art, and folklore. It is a living museum that tells the story of China's past while continuing to inspire future generations with its enduring legacy."""
    #
    # review = read(text)
    # logger.notice("--------review:")
    # logger.notice(review)
    # # Convert text to dictionary
    # result_dict = parse_review_to_dict(review)
    # logger.notice(result_dict.get('review'))
    # i = 0
    # while i < len(result_dict.get('problems')):
    #     problem_list = result_dict.get('problems')
    #     logger.notice(problem_list[i])
    #     i += 1

    article = "Article: Interstellar, directed by Christopher Nolan and co-written with his brother Jonathan, is a 2014 epic science fiction drama that delves into the genre of speculative fiction. The film's narrative is set against the backdrop of a dystopian future where Earth faces catastrophic blight and famine, necessitating a desperate search for a new home for humanity. This setting provides the foundation for a story that blends hard science fiction with emotional human drama.The genre of Interstellar can be categorized as speculative fiction due to its exploration of theoretical physics and its imaginative portrayal of future technologies and space travel. Theoretical physicist Kip Thorne's involvement as an executive producer and scientific consultant adds credibility to the film's scientific underpinnings, making it more than just a typical space adventure. Thorne's work on wormholes and gravitational theories is intricately woven into the plot, enhancing the film's speculative nature.Moreover, Interstellar's genre is further enriched by its thematic elements of love, sacrifice, and survival. The film not only speculates about the future of humanity but also examines the profound connections between individuals and their impact on each other across vast distances and time. This blend of scientific speculation and human emotion sets Interstellar apart from other science fiction films, making it a unique entry in the genre.In summary, Interstellar exemplifies speculative fiction through its ambitious narrative that combines cutting-edge scientific concepts with deeply personal human stories. This fusion creates a compelling cinematic experience that resonates both intellectually and emotionally, solidifying its place within the genre of speculative fiction."
    #read_prompt_list = get_prompts(read_prompts)
    task = "Write an article introducing 'Interstellar'"
    input = """The profound themes of love, time, and human resilience are intricately woven into the fabric of "Interstellar," making it a deeply emotional and intellectually stimulating experience. The film masterfully explores the transcendent nature of love that defies the boundaries of time and space, as exemplified by Cooper's unwavering devotion to his daughter Murph. This bond becomes a central narrative thread, resonating with audiences on a profoundly emotional level. Time dilation, a cornerstone of the film's plot, is depicted with scientific accuracy, thanks to Christopher Nolan's collaboration with theoretical physicist Kip Thorne. The relativity of time creates heart-wrenching scenarios where years pass on Earth while mere hours elapse for the astronauts, challenging their understanding of reality and deepening their emotional struggles. Human resilience is another prevailing theme, showcased through the crew's relentless determination to overcome insurmountable odds in their quest for a new home for humanity. "Interstellar" not only captivates with its awe-inspiring visuals but also leaves a lasting impact by delving into the complexities of human emotions and the indomitable spirit of exploration."""
    titile = "Summary and Personal Reflections on 'Interstellar'"
    reviews1 = readers(task, titile, article)
    logger.notice("groups1----------" + "\n".join(reviews1))
    reviews2 = readers_concurrency(task, titile, article)
    #reviews2 = read(article)

    logger.notice("groups2_c----------" + "\n".join(reviews2))
    #print("one read----------" + reviews2)
