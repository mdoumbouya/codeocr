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

from ratelimit import limits, sleep_and_retry
import base64


load_dotenv()

logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

logging.basicConfig(filename=os.path.join(logs_dir, 'lm_class.log'), 
                    level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def backoff_hdlr(details):
    logging.warning("Backing off {wait:0.1f} seconds after {tries} tries calling function {target} with args {args} and kwargs {kwargs}".format(**details))


logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
GPT_MODEL = "gpt-4-0613"

# Define rate limit
ONE_MINUTE = 60

class LMPostCorrectionAlgorithm(object):
    def __init__(self, name):
        self.name = name
        
    @sleep_and_retry
    @limits(calls=40, period=ONE_MINUTE)
    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
    def post_correction(self, document_metadata):
        raise NotImplementedError()

# The none method, it does nothing to the code
class no_lmpc(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("no-lmpc")
        
    def post_correction(self, document_metadata):
        updated_document_metadata = copy.deepcopy(document_metadata)
        ir_algo_output_code = updated_document_metadata["ir_algo_output_code"]
        return ir_algo_output_code

# Chain of thought Class
class COTprompting(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("cot-v1")
        
    @sleep_and_retry
    @limits(calls=40, period=ONE_MINUTE)
    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
    def post_correction(self, document_metadata):
        
        updated_document_metadata = copy.deepcopy(document_metadata)
        ir_algo_output_code = updated_document_metadata["ir_algo_output_code"]

        lm_post_processed_code = triple_prompt(ir_algo_output_code)
        return lm_post_processed_code
        
class COTprompting_test1(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("cot-v1-tes1")
        
    @sleep_and_retry
    @limits(calls=40, period=ONE_MINUTE)
    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
    def post_correction(self, document_metadata):
        
        updated_document_metadata = copy.deepcopy(document_metadata)
        ir_algo_output_code = updated_document_metadata["ir_algo_output_code"]

        lm_post_processed_code = triple_prompt_test1(ir_algo_output_code)
        return lm_post_processed_code
        
class COTprompting_test2(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("cot-v1-test2")
        
    @sleep_and_retry
    @limits(calls=40, period=ONE_MINUTE)
    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
    def post_correction(self, document_metadata):
        
        updated_document_metadata = copy.deepcopy(document_metadata)
        ir_algo_output_code = updated_document_metadata["ir_algo_output_code"]

        lm_post_processed_code = triple_prompt_test2(ir_algo_output_code)
        return lm_post_processed_code
        
class COTprompting_test3(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("cot-v1-test3")
        
    @sleep_and_retry
    @limits(calls=40, period=ONE_MINUTE)
    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
    def post_correction(self, document_metadata):
        
        updated_document_metadata = copy.deepcopy(document_metadata)
        ir_algo_output_code = updated_document_metadata["ir_algo_output_code"]

        lm_post_processed_code = triple_prompt_test3(ir_algo_output_code)
        return lm_post_processed_code

class COTprompting_test4(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("cot-v1-test4")
        
    @sleep_and_retry
    @limits(calls=40, period=ONE_MINUTE)
    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
    def post_correction(self, document_metadata):
        
        updated_document_metadata = copy.deepcopy(document_metadata)
        ir_algo_output_code = updated_document_metadata["ir_algo_output_code"]

        lm_post_processed_code = triple_prompt_test4(ir_algo_output_code)
        return lm_post_processed_code
    
class COTprompting_test5(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("cot-v1-test5")
        
    @sleep_and_retry
    @limits(calls=40, period=ONE_MINUTE)
    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
    def post_correction(self, document_metadata):
        
        updated_document_metadata = copy.deepcopy(document_metadata)
        ir_algo_output_code = updated_document_metadata["ir_algo_output_code"]

        lm_post_processed_code = triple_prompt_test5(ir_algo_output_code)
        return lm_post_processed_code



# Simple Prompting Classes
class SIMPLEprompting(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("simple-v1")
        
    @sleep_and_retry
    @limits(calls=40, period=ONE_MINUTE)
    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
    def post_correction(self, document_metadata):
        
        updated_document_metadata = copy.deepcopy(document_metadata)
        ir_algo_output_code = updated_document_metadata["ir_algo_output_code"]
        
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant who helps correct OCR result of handwritten python code.",
            },
            {
                "role": "user",
                "content": f"""
Only fix typos in the following code. Do not change anything else. Here is the code:
{ir_algo_output_code}

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
            "temperature": 0.0,
        }

        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Raises a HTTPError if the response was an HTTP 4xx or 5xx
            response_json = response.json()
            result = remove_blank_lines(extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip()))
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

class SIMPLEprompting_test1(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("simple-v1-test1")
        
    @sleep_and_retry
    @limits(calls=40, period=ONE_MINUTE)
    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
    def post_correction(self, document_metadata):
        
        updated_document_metadata = copy.deepcopy(document_metadata)
        ir_algo_output_code = updated_document_metadata["ir_algo_output_code"]
        
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant who helps correct OCR result of handwritten python code.",
            },
            {
                "role": "user",
                "content": f"""
Only fix typos in the following code. Do not change anything else. Here is the code:
{ir_algo_output_code}

return code in the following format:
```python
Code goes here
```
*VERY IMPORTANT NOTE*
- Do not fix any logical error of the original code
- Do not fix any indentation of the original code
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
            "temperature": 0.0,
        }

        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Raises a HTTPError if the response was an HTTP 4xx or 5xx
            response_json = response.json()
            result = remove_blank_lines(extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip()))
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


class SIMPLEprompting_test2(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("simple-v1-test2")
        
    @sleep_and_retry
    @limits(calls=40, period=ONE_MINUTE)
    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
    def post_correction(self, document_metadata):
        
        updated_document_metadata = copy.deepcopy(document_metadata)
        ir_algo_output_code = updated_document_metadata["ir_algo_output_code"]
        
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant who helps correct OCR result of handwritten python code.",
            },
            {
                "role": "user",
                "content": f"""
Only fix typos in the following code, and errors, and garbage text that may come from a Optical Character Recongnition system. Do not change anything else about the code. Here is the code:
{ir_algo_output_code}

return code in the following format:
```python
Code goes here
```
*VERY STRICT RULE*
- Do not fix any logical, or numerical error of the original code.
- Do not fix any indentation of the original code.
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
            "temperature": 0.0,
        }

        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Raises a HTTPError if the response was an HTTP 4xx or 5xx
            response_json = response.json()
            result = remove_blank_lines(extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip()))
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


class SIMPLEprompting_test3(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("simple-v1-test3")
        
    @sleep_and_retry
    @limits(calls=40, period=ONE_MINUTE)
    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
    def post_correction(self, document_metadata):
        
        updated_document_metadata = copy.deepcopy(document_metadata)
        ir_algo_output_code = updated_document_metadata["ir_algo_output_code"]
        
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant who helps correct OCR result of handwritten python code.",
            },
            {
                "role": "user",
                "content": f"""
Only fix typos in the following code, and errors, and garbage text that may come from a Optical Charracter Recongnition system. Here is the code:
{ir_algo_output_code}

return code in the following format:
```python
Code goes here
```
*VERY STRICT RULE*
- Do not fix any logical, or numerical error of the original code
- Do not change any indentation of the original code. 
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
            "temperature": 0.0,
        }

        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Raises a HTTPError if the response was an HTTP 4xx or 5xx
            response_json = response.json()
            result = remove_blank_lines(extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip()))
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


# Gpt 4 vision

class GPT4_Vision(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("gpt4-vision")
        
    @sleep_and_retry
    @limits(calls=40, period=ONE_MINUTE)
    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
    def post_correction(self, image_path):
        try:
            encoded_image = encode_image(image_path)
            response_json = call_gpt4v_api(encoded_image)
            result = remove_blank_lines(extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip()))
            return result


        except Exception as e:
            print(f"Unexpected error in get_gpt4v_extraction: {e}")
            logger.error(f"Unexpected error in get_gpt4v_extraction: {e}")






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
    try:
        first_tilda = txt.find("```")
        second_tilda = txt.find("```", first_tilda + 1)
        if first_tilda != -1 and second_tilda != -1:
            code_lang = txt[first_tilda + 3: first_tilda + 9]
            if code_lang in ["python", "Python"]:
                return txt[first_tilda + 9:second_tilda].strip()
            return txt[first_tilda + 3:second_tilda].strip()
        return txt
    except Exception as e:
        logger.error(f"Error in clear_response: {e}")
        return txt  # return original text in case of error














"""
Functions for prompting in COT
"""


@sleep_and_retry
@limits(calls=20, period=ONE_MINUTE)
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
        result = remove_blank_lines(extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip()))
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


@sleep_and_retry
@limits(calls=20, period=ONE_MINUTE)
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
        result = remove_blank_lines(extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip()))
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


@sleep_and_retry
@limits(calls=20, period=ONE_MINUTE)
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
        result = remove_blank_lines(extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip()))
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

@sleep_and_retry
@limits(calls=20, period=ONE_MINUTE)
@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def triple_prompt_test1(entire_code, temperature=0.0):
    initial_LM_code = initial_prompt(entire_code)
    # time.sleep(3)
    double_prompted_code = double_prompt(initial_LM_code)
    # time.sleep(3)
    
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
            "content": "Do not change the original indentation, keep the indentation same as the original input. Only fix the typos in code.",
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
        result = remove_blank_lines(extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip()))
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

@sleep_and_retry
@limits(calls=20, period=ONE_MINUTE)
@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def triple_prompt_test2(entire_code, temperature=0.0):
    initial_LM_code = initial_prompt(entire_code)
    # time.sleep(3)
    double_prompted_code = double_prompt(initial_LM_code)
    # time.sleep(3)
    
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
            "content": "Do not change the original indentation, keep the indentation same as the original code.",
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
        result = remove_blank_lines(extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip()))
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


@sleep_and_retry
@limits(calls=20, period=ONE_MINUTE)
@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def triple_prompt_test3(entire_code, temperature=0.0):
    initial_LM_code = initial_prompt(entire_code)
    # time.sleep(3)
    double_prompted_code = double_prompt(initial_LM_code)
    # time.sleep(3)
    
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
            "content": "Do not change the original input code's indentation.",
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
        result = remove_blank_lines(extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip()))
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

@sleep_and_retry
@limits(calls=20, period=ONE_MINUTE)
@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def triple_prompt_test4(entire_code, temperature=0.0):
    initial_LM_code = initial_prompt(entire_code)
    # time.sleep(3)
    double_prompted_code = double_prompt(initial_LM_code)
    # time.sleep(3)
    
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
            "content": "Do not change the original input code's indentation. Only fix the typos in code.",
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
        result = remove_blank_lines(extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip()))
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

@sleep_and_retry
@limits(calls=20, period=ONE_MINUTE)
@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def triple_prompt_test5(entire_code, temperature=0.0):
    initial_LM_code = initial_prompt(entire_code)
    # time.sleep(3)
    double_prompted_code = double_prompt(initial_LM_code)
    # time.sleep(3)
    
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
            "content": "Do not change the original input code's indentation. Only fix errors that might happen in a OCR Pipeline.",
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
        result = remove_blank_lines(extract_code_from_codeBlock(response_json["choices"][0]["message"]["content"].strip()))
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



# GPT4 Vision Setup
def encode_image(image_path):
    """
    Encode a local image file to base64.
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error in encode_image: {e}")


@sleep_and_retry
@limits(calls=40, period=ONE_MINUTE)
@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def call_gpt4v_api(encoded_image):
        api_key = OPENAI_API_KEY
        if not api_key:
            logger.error("OPENAI_API_KEY not set in environment variables")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages":[
            {
                "role": "user",
                "content": [
                    {"type": "text", 
                    "text": """The image contains handwritten python code.  
return the code in the image in this below codeblock format:

```python
code
```

Only fix typos in the code.
*VERY STRICT RULE*
- Do not fix any logical, or numerical error of the original code. KEEP THE LOGIC EXACTLY AS IT IS, even if it is wrong. 
- Do not change any indentation from the original image. KEEP THE INDENTATION EXACTLY AS IT IS, even if it is wrong.
"""},
                {
                    "type": "image_url",
                    "image_url": {
                    "url":f"data:image/jpeg;base64,{encoded_image}",
                },
                },
            ],
            }
        ],
            "max_tokens": 1500
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=15)

        if response.status_code == 200:
            json_response = response.json()
            return json_response
        else:
            logger.error(f"Error from GPT-4 API: {response.text}")
