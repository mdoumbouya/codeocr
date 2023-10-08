import logging
import copy
import numpy as np
from code_ocr.global_utils import avg_list
import requests
import json
import openai
import backoff
import os
from dotenv import load_dotenv
import time

load_dotenv()

logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

logging.basicConfig(filename=os.path.join(logs_dir, 'lm_class.log'), 
                    level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
GPT_MODEL = "gpt-4-0613"

class LMPostCorrectionAlgorithm(object):
    def __init__(self, name):
        self.name = name
        
    def post_correction(self, document_metadata):
        raise NotImplementedError()


# Chain of thought Class
class COTprompting(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("cot-v1")
        
    def post_correction(self, document_metadata):
        
        updated_document_metadata = copy.deepcopy(document_metadata)
        ir_algo_output_code = updated_document_metadata["ir_algo_output_code"]

        lm_post_processed_code = triple_prompt(ir_algo_output_code)
        return lm_post_processed_code
        
        
        
# Simple Class
class SIMPLEprompting(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("simple-v1")
        
    def post_correction(self, document_metadata):
        
        updated_document_metadata = copy.deepcopy(document_metadata)
        ir_algo_output_code = updated_document_metadata["ir_algo_output_code"]
        
        lm_post_processed_code = simple_prompt(ir_algo_output_code)
            
        return lm_post_processed_code

def remove_blank_lines(code):
    code = str(code)
    lines = code.split("\n")
    cleaned_code = ""
    for index, line in enumerate(lines):
        if line.strip() == "":
            if index != 0:
                if index + 1 < len(lines):
                    next_line = lines[index + 1].strip()
                    if next_line.startswith(("def ", "class ", "@", 'if __name__ == "__main__":')):
                        cleaned_code += "\n"
        else:
            if line.strip().startswith(("def ", "class ", "@", 'if __name__ == "__main__":')):
                
                if index > 0 and lines[index - 1].strip() != "":
                    cleaned_code += "\n"
            cleaned_code += line + "\n"
    return cleaned_code

def extract_code_from_codeBlock(txt):
    """
    Extracts code blocks from a given text string and returns the code as a string.

    Args:
        txt (str): The text string to extract code blocks from.

    Returns:
        str: The extracted code block as a string, or the original text if no code block was found.
    """
    first_tilda = txt.find("```")
    if first_tilda != -1:
        second_tilda = txt.find("```", first_tilda + 1)
        if second_tilda != -1:
            if txt[first_tilda + 3: first_tilda + 9] == "python" or txt[first_tilda + 3: first_tilda + 9] == "Python":
                return txt[first_tilda + 9:second_tilda]
            else:
                return txt[first_tilda + 3:second_tilda]
    return txt

def backoff_hdlr(details):
    logging.warning("Backing off {wait:0.1f} seconds after {tries} tries calling function {target} with args {args} and kwargs {kwargs}".format(**details))

@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def initial_prompt(entire_code, temperature=0.0):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who helps translate OCR result of handwritten python code from OCR output",
        },
        {
            "role": "user",
            "content": f"""
**OCR Output for CODE**
{entire_code}

**Instruction**
Only correct all spelling mistakes in the code. Do not fix any logical error. Do not fix any indentation. 


return code in the following format:
```python
code goes here.
```
""",
        },
    ]
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    payload = {
        "model": GPT_MODEL,
        "messages": messages,
        "max_tokens": 2042,
        "temperature": temperature,
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises a HTTPError if the response was an HTTP 4xx or 5xx
        response_json = response.json()
        result = extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip())
        return result
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error: {errh}")
        return "failed"
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Error Connecting: {errc}")
        return "failed"
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")
        return "failed"
    except requests.exceptions.RequestException as err:
        logging.error(f"Something went wrong with the request: {err}")
        return "failed"
    except Exception as e:
        logging.error(f"Unknown error: {e}")
        return "failed"

@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def double_prompt(entire_code, temperature=0.0):
    initial_LM_code = initial_prompt(entire_code)
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who helps translate OCR result of handwritten python code from OCR output",
        },
        {
            "role": "user",
            "content": f"""
**OCR Output for CODE**
{entire_code}

**Instruction**
Only correct all spelling mistakes in the code. Do not fix any logical error. Do not fix any indentation. 


return code in the following format:
```python
code goes here.
```
""",
        },
        {
            "role": "assistant",
            "content": initial_LM_code,
        },
        {
            "role": "user",
            "content": f"""do not fix the logical errors""",
        }
    ]
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    payload = {
        "model": GPT_MODEL,
        "messages": messages,
        "max_tokens": 2042,
        "temperature": temperature,
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises a HTTPError if the response was an HTTP 4xx or 5xx
        response_json = response.json()
        result = extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip())
        return result
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error: {errh}")
        return "failed"
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Error Connecting: {errc}")
        return "failed"
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")
        return "failed"
    except requests.exceptions.RequestException as err:
        logging.error(f"Something went wrong with the request: {err}")
        return "failed"
    except Exception as e:
        logging.error(f"Unknown error: {e}")
        return "failed"

@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def triple_prompt(entire_code, temperature=0.0):
    initial_LM_code = initial_prompt(entire_code)
    time.sleep(3)
    double_prompted_code = double_prompt(initial_LM_code)
    time.sleep(3)
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who helps translate OCR result of handwritten python code from OCR output",
        },
        {
            "role": "user",
            "content": f"""
**OCR Output for CODE**
{entire_code}

**Instruction**
Only correct all spelling mistakes in the code. Do not fix any logical error. Do not fix any indentation. 


return code in the following format:
```python
code goes here.
```
""",
        },
        {
            "role": "assistant",
            "content": initial_LM_code,
        },
        {
            "role": "user",
            "content": f"""do not fix the logical errors""",
        },
        {
            "role": "assistant",
            "content": double_prompted_code,
        },
        {
            "role": "user",
            "content": "Do not change the original indentation, keep it the same as the OCR output",
        }
    ]
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    payload = {
        "model": GPT_MODEL,
        "messages": messages,
        "max_tokens": 2042,
        "temperature": temperature,
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises a HTTPError if the response was an HTTP 4xx or 5xx
        response_json = response.json()
        result = extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip())
        return result
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error: {errh}")
        return "failed"
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Error Connecting: {errc}")
        return "failed"
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")
        return "failed"
    except requests.exceptions.RequestException as err:
        logging.error(f"Something went wrong with the request: {err}")
        return "failed"
    except Exception as e:
        logging.error(f"Unknown error: {e}")
        return "failed"

@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def simple_prompt(entire_code, temperature=0.0):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who helps correct OCR result of handwritten python code.",
        },
        {
            "role": "user",
            "content": f"""
Only fix typos in the following code. Do not change anything else. Here is the code:
{entire_code}

return code in the following format:
```python
Code goes here
```
""",
        },
    ]
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    payload = {
        "model": GPT_MODEL,
        "messages": messages,
        "max_tokens": 2042,
        "temperature": temperature,
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises a HTTPError if the response was an HTTP 4xx or 5xx
        response_json = response.json()
        result = extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip())
        return result
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error: {errh}")
        return "failed"
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Error Connecting: {errc}")
        return "failed"
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")
        return "failed"
    except requests.exceptions.RequestException as err:
        logging.error(f"Something went wrong with the request: {err}")
        return "failed"
    except Exception as e:
        logging.error(f"Unknown error: {e}")
        return "failed"