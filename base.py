import json

import openai
from openai import OpenAI,AzureOpenAI
import requests
import requests, re
import os
from logger_config import get_logger

logger = get_logger()

Model = "deepseek-chat"
client = OpenAI(api_key= 'API_KEY', base_url= 'BASE_URL')

def load_config(config_path="config.json"):
    """Load the model configuration from a JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件未找到：{config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def set_model(model_name = 'deepseek', config_path="config.json"):
    """
       Set the model and initialize the OpenAI-compatible client
       using model-specific configuration from a JSON config file.
       """

    global client
    global Model
    config = load_config(config_path)

    if model_name not in config:
        logger.error(f"Model name error: {model_name} not found in config file.")
        raise ValueError(f"Invalid model name: {model_name}")

    model_config = config[model_name]
    api_key = model_config.get("api_key")
    base_url = model_config.get("base_url")
    Model = model_config.get("model")

    if not api_key or not Model:
        logger.error(f"Incomplete configuration for model: {model_name}")
        raise ValueError(f"Incomplete configuration for model: {model_name}")

    # Initialize client with or without a custom base_url
    if base_url:
        client = OpenAI(api_key=api_key, base_url=base_url)
    else:
        client = OpenAI(api_key=api_key)

    logger.info(f"Model set to: {Model}")

def callLLM(query, temperature=0.5):
    test = None
    while test is None:
        try:
            response = client.chat.completions.create(
                model= Model,
                messages=[
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                stream=False,
                temperature=temperature,
                frequency_penalty=1
            )

            # response = openai.ChatCompletion.create(
            #     model="gpt-4",
            #     messages=[
            #         {
            #             "role": "user",
            #             "content": query
            #         }
            #     ],
            #     temperature=temperature,
            #     frequency_penalty=0.7
            # )
            test = response.choices[0].message.content
        except Exception as i:
            logger.error(i)
    return test

def callLLM_with_file(prompt,text, temperature=0.5):
    llm_response = None
    while llm_response is None:
        try:
            response = client.chat.completions.create(
                model=Model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                temperature=temperature,
            )
            llm_response = response.choices[0].message.content
        except Exception as i:
            logger.error(i)
    return llm_response


# def callLLM(query, temperature=0.75):
#     test = None
#     while test is None:
#         try:
#             access_token = "24.39e5512a3ddff9445e372b917f90c243.2592000.1694608929.282335-34290760"
#             # url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ebsft4sc_0810?access_token={access_token}"
#             url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/hajd_sc_sft_0821?access_token={access_token}"
#             # url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token={access_token}"
#             payload = json.dumps({
#                 # chat
#                 "messages": [
#                     {
#                         "role": "user",
#                         "content": query[:2000],
#                         "temperature": 0.75
#                     }
#                 ],
#                 "stream": False,
#                 "temperature": 0.75
#             })
#             headers = {
#                 'Content-Type': 'application/json'
#             }
#             # print("Calling LLM")
#             response = requests.request("POST", url, headers=headers, data=payload)
#             # print("Finish calling LLM")
#             test = json.loads(response.text)['result']
#         except:
#             pass
#     return test


def clean_text(text):
    # Remove escape characters and extra spaces from text
    text = text.replace("\n", " ").replace("\r", " ")
    text = ' '.join(text.split())
    return text

def clean_text_symbol(text):
    # Clear special symbols from text
    text = text.replace("\\", "").replace("*", "").replace("#", "")
    text = re.sub(r'[ \t]+', ' ', text)
    return text

def seperate_text(content, length):
    text_seg = re.split("\\.", content)
    res = []
    cache_text = ""
    for t in text_seg:
        t  = clean_text(t)
        cache_text = cache_text + t + "."
        if len(cache_text.split()) >= length:
            res.append(cache_text)
            cache_text = ""
    if len(cache_text.split()) > 0:
        res.append(cache_text)
    return res
# Split into a list by line and remove empty lines

def split_into_list(input_string):
    # Remove blank lines
    return [line for line in input_string.splitlines() if line.strip()]

def save_to_txt(filename, text):

    # Save the input text to the specified txt file.
    #
    # :param filename: the name of the saved file
    # :param text: the text content to be saved

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)
    #print(f"Text saved to {filename}")


def read_from_txt(filename):
    # Read the contents from the specified txt file. If the file does not exist, create a blank file.
    #
    # :param filename: the file name to read
    # :return: a string containing the file contents
    # Check if the file exists在
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as file:
            # Create a blank file
            pass
    # Read file contents
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read().strip().split("\n")
    return content

def callGPT(query, temperature=0.7):
    response = client.chat.completions.create(
        model="gpt-4",  # Model deployment name.
        messages=[

            # This message triggers the model to reply
            {"role": "user", "content": query
             }
        ]
    )
    message = response.choices[0].message.content
    print(message)
    return message

if __name__ == "__main__":
    set_model("deepseek")
    query = 'who are you?'
    result = callLLM(query)
    print(result)