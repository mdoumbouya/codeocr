import copy
import numpy as np
from code_ocr.global_utils import avg_list
import requests
import json
import openai
import backoff
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
GPT_MODEL = "gpt-4-0613"

class LMPostCorrectionAlgorithm(object):
    def __init__(self, name):
        self.name = name
        
    def post_correction(self, document_metadata):
        raise NotImplementedError()



class COTprompting(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("cot-v1")
        
    def post_correction(self, document_metadata):
        updated_document_metadata = copy.deepcopy(document_metadata)
        
        ir_algo_output_code = updated_document_metadata["ir_algo_output_code"]
        
        lm_post_processed_code = triple_prompt(ir_algo_output_code)
            
        return lm_post_processed_code
        
        
# Double prompting function







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

# Takes in a string as an input, and outputs the string with the code block removed
def clear_response(txt):

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
    print("Backing off {wait:0.1f} seconds after {tries} tries calling function {target} with args {args} and kwargs {kwargs}".format(**details))



@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def initial_prompt(entire_code, temperature=0.0):
    # print("Into the post process gpt function")
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
        # print("trying GPT")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            # print("GPT worked")
            response_json = response.json()
            # print(response_json)
            result = response_json["choices"][0]["message"]["content"].strip()
            
        
            return result
        else:
            print("GPT failed")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""



@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def double_prompt(entire_code, temperature=0.0):
    # print("Into the post process gpt function")
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
        # print("trying GPT")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            # print("GPT worked")
            response_json = response.json()
            # print(response_json)
            result = remove_blank_lines(clear_response(response_json["choices"][0]["message"]["content"].strip()))
            return result
        
        else:
            print("GPT failed")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""


@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def triple_prompt(entire_code, temperature=0.0):
    # print("Into the post process gpt function")
    initial_LM_code = initial_prompt(entire_code)
    double_prompted_code = double_prompt(initial_LM_code)
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
        # print("trying GPT")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            # print("GPT worked")
            response_json = response.json()
            # print(response_json)
            result = remove_blank_lines(clear_response(response_json["choices"][0]["message"]["content"].strip()))
            return result
        
        else:
            print("GPT failed")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

