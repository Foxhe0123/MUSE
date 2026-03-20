import requests, re
from bs4 import BeautifulSoup
import time

#from duckduckgo_search import DDGS
from ddgs import DDGS
from newspaper import Article
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import numpy as np
from collections import Counter
from selenium.webdriver.chrome.service import Service
from sentence_transformers import SentenceTransformer
from webdriver_manager.chrome import ChromeDriverManager
from base import clean_text,seperate_text
from logger_config import get_logger

# Get the configured logger
logger = get_logger()


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

latestchromedriver = ChromeDriverManager().install()
service = Service(executable_path=latestchromedriver)
logger.notice(latestchromedriver)

def cos_sim(str1, str2):
    # str1 = jieba.lcut(str1)
    # str2 = jieba.lcut(str2)
    co_str1 = (Counter(str1))
    co_str2 = (Counter(str2))
    p_str1 = []
    p_str2 = []
    for temp in set(str1 + str2):
        p_str1.append(co_str1[temp])
        p_str2.append(co_str2[temp])
    p_str1 = np.array(p_str1)
    p_str2 = np.array(p_str2)
    return p_str1.dot(p_str2) / (np.sqrt(p_str1.dot(p_str1)) * np.sqrt(p_str2.dot(p_str2)))


def baidu_search(keyword):
    results = []
    wait_sleep = 0
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(service=service, options=options)
    while len(results) == 0:
        try:
            time.sleep(wait_sleep)
            wait_sleep += 2

            r = re.compile('<h3[\\s\\S]*?<a[^>]*?href[^>]*?"(.*?)"[^>]*?>(.*?)</a>')
            url = "https://www.baidu.com"
            browser.get(url)
            search_box = browser.find_element(By.CSS_SELECTOR, '#kw')
            search_box.send_keys(keyword)
            submit_button = browser.find_element(By.CSS_SELECTOR, '#su')
            submit_button.click()
        except:
            continue
        scroll_pause_time = 1
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        for i in r.findall(browser.page_source):
            if "http" in i[0]:
                results.append([re.compile('<.*?>').sub('', i[1]), i[0]])
    browser.quit()
    new_results = []
    for r in results:
        new_results.append(r[1])
    return new_results


def google_search(keyword):
    results = []
    wait_sleep = 1
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(service=service, options=options)
    while len(results) == 0:
        try:
            r = re.compile('<h3[\\s\\S]*?<a[^>]*?href[^>]*?"(.*?)"[^>]*?>(.*?)</a>')
            url = "https://www.google.com.hk/"
            browser.get(url)
            search_box = browser.find_element(by='name', value='q')
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.RETURN)
            time.sleep(wait_sleep)
            wait_sleep += 2
        except:
            continue
        scroll_pause_time = 1
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        for i in r.findall(browser.page_source):
            if ("http" in i[0]) and ("translate" not in i[0]):
                results.append([re.compile('<.*?>').sub('', i[1]), i[0]])
    browser.quit()
    new_results = []
    for r in results:
        if r[1][:4] == "http":
            new_results.append(r[1])
    return new_results

def duckdukcgo_search(keyword):
    url_list = []
    results = []
    try:
        results = DDGS().text(keyword, region='us-en', safesearch='off', timelimit='y',backend='auto', max_results=15)
        # Searching for pdf files
        # results = DDGS().text('russia filetype:pdf', region='wt-wt', safesearch='off', timelimit='y', max_results=10)

        for l_i in range(len(results)):
            url_list.append(results[l_i].get('href'))
            logger.info(
                str(l_i + 1) + '.' + results[l_i].get('href') + '\n--' + results[l_i].get('title') + '\n--' + results[
                    l_i].get('body'))
    except Exception as e:
        logger.warning(f"Error: {e}")
    return url_list

def search_content(keyword):
    content = {}
    try:
        results = DDGS().text(keyword, region='us-en', safesearch='off', timelimit='y',backend='auto', max_results=15)
        # Searching for pdf files
        # results = DDGS().text('russia filetype:pdf', region='wt-wt', safesearch='off', timelimit='y', max_results=10)

        for l_i in range(len(results)):
            logger.info(
                str(l_i + 1) + '.' + results[l_i].get('href') + '\n--' + results[l_i].get('title') + '\n--' + results[
                    l_i].get('body'))
            content[results[l_i].get('title')] = results[l_i].get('body')
    except Exception as e:
        logger.warning(f"Error: {e}")
    return content

def get_dynamic_content(url):
    # Set up Selenium WebDriver (Make sure to have ChromeDriver installed and in your PATH)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    time.sleep(3)  # Adjust sleep time as necessary to allow content to load
    # Handling Cookies
    cookies = driver.get_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)

    # Reload the page
    driver.get(url)
    time.sleep(5)
    # Try to click on "show more" buttons or similar to expand content
    try:
        while True:
            show_more_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '展开阅读全文')]")
            if not show_more_buttons:
                break
            for button in show_more_buttons:
                driver.execute_script("arguments[0].click();", button)
                time.sleep(1)
    except Exception as e:
        logger.warning(f"Error clicking show more buttons: {e}")

    page_source = driver.page_source
    driver.quit()
    return page_source

def extract_text_from_url(url, keyword):
    try:
        # Use selenium to get dynamic content
        page_content = get_dynamic_content(url)
    except Exception as e:
        logger.warning(f"Error fetching the URL {url}: {e}")
        return None

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')

    # Remove unnecessary tags
    for unnecessary_tag in soup(['a' 'script', 'style', 'header', 'footer', 'nav', 'aside']):
        unnecessary_tag.extract()

    # Find all blocks of text (usually within <p> tags)
    text_blocks = soup.find_all(['p','blockquote'])

    # Set up a list of related content
    #relevant_content = []
    block_texts = ''
    for block in text_blocks:
        block_text = block.get_text()
        block_text = clean_text(block_text)

        # Extract sentences with keywords
        # Split text into sentences
        #sentences = re.split(r'(?<=[.!?]) +', block_text)
        # Filter sentences to keep those that contain at least one keyword
        #relevant_sentences = [sentence for sentence in sentences if any(keyword.lower() in sentence.lower() for keyword in keywords)]
        #if relevant_sentences:
            #relevant_content.extend(relevant_sentences)
            #relevant_content.append(' '.join(relevant_sentences))

        block_texts += block_text

    return block_texts

def get_web_text(url_list, keywords):
    contents = []
    #summarys_list = []
    #Summarys = ''
    #si = 1
    for url in url_list:
        try:
            # Use newspaper3k library's Article to extract the text content
            article = Article(url)
            article.download()
            article.parse()
            #article.nlp()
            #print("########Summary:"+article.summary)
            #if article.summary:
                #Summarys += str(si)+ '. '+ article.summary + '\n'
                #si += 1
            content = article.text
            #print(f"-URL: {url}\nExtracted Content:\n{content}\n{'=' * 80}\n")
            # If newspaper3k cannot effectively extract the content, use BeautifulSoup to extract it
            if not content.strip() or content.strip().__len__() < 500:
                text_content = extract_text_from_url(url, keywords)
                if text_content:
                    contents.append(text_content)
                    #summarys_list.append(text_content)
                    #print(f"--URL: {url}\nExtracted Content:\n{text_content}\n{'=' * 80}\n")
            else:
                contents.append(content)
                #summarys_list.append(article.summary)

        except Exception as e:
            # Error: Article `download()` failed with HTTPSConnectionPool
            logger.info(f"Error: {e}")

            # text_content = extract_text_from_url(url, keywords)
            # if text_content:
            #     contents.append(text_content)
                #summarys_list.append(text_content)

                #print(f"---URL: {url}\nExtracted Content:\n{text_content}\n{'=' * 80}\n")
    return contents

#获取文本相似度
def get_text_sim(text1, text2):
    # 1. Load a pretrained Sentence Transformer model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # The sentences to encode
    sentences = [text1]
    if isinstance(text2, str):  # If text2 is a string
        sentences.append(text2)
    elif isinstance(text2, list):  # If text2 is a list of strings
        sentences.extend(text2)

    # 2. Calculate embeddings by calling model.encode()
    embeddings = model.encode(sentences)

    # 3. Calculate the embedding similarities
    similarities = model.similarity(embeddings, embeddings)

    #logger.info(similarities)
    # 4. get similarities
    # Convert to NumPy array
    np_matrix = similarities.numpy()

    # Extract the first column and remove the first row
    first_column_excluding_first_row = np_matrix[1:, 0]
    # Calculate the average
    average_sim = np.mean(first_column_excluding_first_row)
    return average_sim


# Filter similar text
def get_simtext(query, page_list, sim):
    # 1. Load a pretrained Sentence Transformer model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # The sentences to encode
    idx = 0
    text = ""
    while len(text.split()) < 1200 and idx < len(page_list):
        page_text = page_list[idx]
        page_text_seg = seperate_text(page_text, 100)
        page_text_seg.insert(0, query)

        # 2. Calculate embeddings by calling model.encode()
        embeddings = model.encode(page_text_seg)

        # 3. Calculate the embedding similarities
        similarities = model.similarity(embeddings, embeddings)

        #logger.info(similarities)
        # 4. get similarities test
        sim_text = []
        for i in range(embeddings.shape[0] - 1):
            if similarities[0][i + 1] >= sim:
                sim_text.append(page_text_seg[i + 1])

        new_text = "".join(sim_text)
        idx += 1
        text += new_text
    return text





def SearchAPI(query, search_func=duckdukcgo_search, search_websites=[]):
    logger.notice(f"Starting web search for {query}...")
    origin_search_results = []
    origin_search_results.append(search_func(query))
    for site in search_websites:
        search_query = query + " site:" + site
        origin_search_results.append(search_func(search_query))
    max_length = max([len(sr) for sr in origin_search_results])
    search_results = []
    for i in range(max_length):
        for s_i in range(len(search_websites)+1):
            if i < len(origin_search_results[s_i]):
                search_results.append(origin_search_results[s_i][i])

    search_results = list(set(search_results))

    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # browser = webdriver.Chrome(service=service, options=options)
    # while len(text.split()) < 800 and idx < len(search_results):
    #     browser.get(search_results[idx])
    #     soup = BeautifulSoup(browser.page_source, 'html.parser')
    #     # url = browser.current_url
    #     page_text = soup.get_text()
    #     page_text = " ".join(page_text.split())
    #     page_text_seg = seperate_text(page_text, 1500)
    #     page_text = ""
    #     for t in page_text_seg:
    #         page_text += callExtract(t)
    #     try:
    #         page_text_seg = seperate_text(page_text, 300)
    #         sim_scores = []
    #         for t in page_text_seg:
    #             sim_scores.append(cos_sim(t, query))
    #         target_idx = np.argmax(sim_scores)
    #         new_text = page_text_seg[target_idx]
    #         text = text + new_text
    #     except:
    #         pass
    #     idx += 1
    # browser.quit()
    content_list = get_web_text(search_results, query)

    #Filter similar content.
    text = get_simtext(query, content_list,0.6)

    return text


def google_search_img(keyword):
    src = None
    while src is None:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser = webdriver.Chrome(service=service, options=options)

        url = 'https://www.google.com.hk/imghp'
        browser.get(url)
        try:
            search_box = browser.find_element(by="name", value='q')
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.RETURN)

            scroll_pause_time = 1
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)

            soup = BeautifulSoup(browser.page_source, 'html.parser')
            img_list = soup.select('img.rg_i')
            for img in img_list:
                src = img['src']
                # if src.startswith('data'):
                    # continue
                # else:
                browser.quit()
                return src
        except:
            time.sleep(3)


def baidu_search_img(keyword):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    url = 'https://image.baidu.com/search/acjson?'
    n = 0
    image_url_list = []
    while len(image_url_list) == 0:
        param = {'tn': 'resultjson_com',
                 'logid': '7603311155072595725',
                 'ipn': 'rj',
                 'ct': 201326592,
                 'is': '',
                 'fp': 'result',
                 'queryWord': keyword,
                 'cl': 2,
                 'lm': -1,
                 'ie': 'utf-8',
                 'oe': 'utf-8',
                 'adpicid': '',
                 'st': -1,
                 'z': '',
                 'ic': '',
                 'hd': '',
                 'latest': '',
                 'copyright': '',
                 'word': keyword,
                 's': '',
                 'se': '',
                 'tab': '',
                 'width': '',
                 'height': '',
                 'face': 0,
                 'istype': 2,
                 'qc': '',
                 'nc': '1',
                 'fr': '',
                 'expermode': '',
                 'force': '',
                 'cg': '',
                 'pn': 30,    # 30-60-90
                 'rn': '30',  # 30
                 'gsm': '1e',
                 '1618827096642': ''
                 }
        request = requests.get(url=url, headers=header, params=param)
        request.encoding = 'utf-8'
        html = request.text
        image_url_list = re.findall('"thumbURL":"(.*?)",', html, re.S)
        time.sleep(3)
    return image_url_list[0]

if __name__ == '__main__':
    duckdukcgo_result = duckdukcgo_search("Ernest Hemingway Introduction introduction to Hemingway's The Old Man and the Sea")
    print(duckdukcgo_result)