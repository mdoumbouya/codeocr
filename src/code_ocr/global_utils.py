from sklearn.cluster import MeanShift, estimate_bandwidth
import numpy as np
import json
import matplotlib.pyplot as plt
import cv2
import requests
import backoff
import base64
import io
import plotly.graph_objs as go
import plotly.offline as po
from flask import Markup
from dotenv import load_dotenv
import openai
import os
import time
import pyrebase
import uuid
import boto3
import timeit

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
from PIL import Image
import sys
import time

from google.cloud import vision
from google.oauth2 import service_account
import google.auth
from google.auth.transport.requests import Request

import tempfile
import black
from black import InvalidInput




load_dotenv()

MATHPIX_APP_ID = os.getenv("MATHPIX_APP_ID")
MATHPIX_APP_KEY = os.getenv("MATHPIX_APP_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
GPT_MODEL = "gpt-4-0613"
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_KEY")



current_dir = os.path.dirname(os.path.realpath(__file__))
print(current_dir)
gcloud_key_path = os.path.join(current_dir, 'gcloud-sacct-cred.json')

gcloud_vision_client = vision.ImageAnnotatorClient.from_service_account_json(gcloud_key_path)




AZURE_computervision_client = ComputerVisionClient(AZURE_ENDPOINT, CognitiveServicesCredentials(AZURE_KEY))

LINE_COLORS =  [
    ((0, 0, 255), 'rgb(255, 0, 0)'),       # red
    ((0, 255, 0), 'rgb(0, 255, 0)'),       # green
    ((255, 0, 0), 'rgb(0, 0, 255)'),       # blue
    ((255, 0, 255), 'rgb(255, 0, 255)'),   # magenta
    ((192, 255, 0), 'rgb(0, 255, 192)'),   # mint green
    ((64, 0, 255), 'rgb(255, 0, 64)'),     # deep pink
    ((128, 255, 255), 'rgb(255, 255, 128)'), # pastel yellow
    ((128, 255, 128), 'rgb(128, 255, 128)'), # pastel green
    ((255, 255, 128), 'rgb(128, 255, 255)'), # pastel cyan
    ((255, 255, 0), 'rgb(0, 255, 255)'),   # cyan
    ((255, 165, 0), 'rgb(0, 165, 255)'),   # orange
    ((255, 105, 180), 'rgb(180, 105, 255)'), # hot pink
    ((255, 64, 0), 'rgb(0, 64, 255)'),     # deep orange
    ((0, 165, 255), 'rgb(255, 165, 0)'),   # light blue
    ((60, 179, 113), 'rgb(113, 179, 60)'), # medium sea green
    ((238, 130, 238), 'rgb(238, 130, 238)'), # violet
    ((245, 222, 179), 'rgb(179, 222, 245)'), # wheat
    ((210, 105, 30), 'rgb(30, 105, 210)'), # chocolate
    ((127, 255, 0), 'rgb(0, 255, 127)'),   # chartreuse
    ((255, 140, 0), 'rgb(0, 140, 255)'),   # dark orange
    ((32, 178, 170), 'rgb(170, 178, 32)'), # light sea green
]




def get_line_color(cluster_id, library='cv2'):
    color = LINE_COLORS[cluster_id % len(LINE_COLORS)]
    return color[0] if library == 'cv2' else color[1]


def backoff_hdlr(details):
    print("Backing off {wait:0.1f} seconds after {tries} tries calling function {target} with args {args} and kwargs {kwargs}".format(**details))

def cluster_indentation(response_data):
    
    data = response_data

    min_x = []
    included_line_data = []

    for line in data["line_data"]:
        if 'cnt' in line:
            if line["included"] == True:
                cnt = line["cnt"]
                min_point = min(cnt, key=lambda point: point[0])
                min_point_idx = line["cnt"].index(min_point)
                min_x.append(min_point[0])
                line["min_point_idx"] = min_point_idx
                included_line_data.append(line)

    data["line_data"] = included_line_data
        
    min_x_np = np.array(min_x).reshape(-1, 1)

    mean_shift = MeanShift(bandwidth=30)

    mean_shift.fit(min_x_np)

    labels = mean_shift.labels_
        
    for i, line in enumerate(data["line_data"]):
        line["cluster_id"] = int(labels[i])
        
    return min_x, labels, data



def visualize_lines(data, image_path):
    
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Get the image height and width
    image_height = data['image_height']
    image_width = data['image_width']

    # Create an empty mask image
    #mask = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    
    for line in data["line_data"]:
        if "cnt" in line:
            
            cnt = np.array(line["cnt"], dtype=np.int32)
            cnt = cnt.reshape((-1, 1, 2))
            cv2.polylines(image, [cnt], True, (255, 0, 0), 2)
            
            circle_point = tuple(line["cnt"][line["min_point_idx"]])
            
            cv2.circle(image, circle_point, 14, get_line_color(line["cluster_id"], 'cv2'), -1)
        
    # Combine the original image and mask
    #combined_image = cv2.addWeighted(image, 0.7, mask, 0.3, 0)
    
    # Show the combined image
    
    # Convert image to base64 to use it as source in an HTML img tag
    retval, buffer = cv2.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')

    return jpg_as_text



def plot_histogram(min_x):
    data = [go.Histogram(x=min_x)]
    layout = go.Layout(title='Distribution of min_x values')
    fig = go.Figure(data=data, layout=layout)
    return po.plot(fig, output_type='div')    # Return as a div to embed in HTML


def plot_clustering(min_x, labels):
    data = [go.Scatter(x=min_x, y=labels, mode='markers',
                        marker=dict(color=[get_line_color(label, 'plotly') for label in labels],
                                    size=8, line=dict(width=1)))]
    layout = go.Layout(title='Clustering results of Mean Shift', xaxis=dict(title='min_x'),
                        yaxis=dict(title='Cluster ID'))
    fig = go.Figure(data=data, layout=layout)
    return po.plot(fig, output_type='div')    # Return as a div to embed in HTML
    
    
# Old MATHPIX indentation processing
def process_indentation(data):
    
    tab = '\t'
    # print(data)
    # print(labels)
        
    label_coord = {}
    label_avg = {}
        
    for line in data["line_data"]:
        if "cluster_id" in line and "min_point_idx" in line:
            cluster_id = line["cluster_id"]
            min_point_idx = line["min_point_idx"]
            if cluster_id not in label_coord:
                label_coord[cluster_id] = []
            label_coord[cluster_id].append(line["cnt"][min_point_idx][0])
        
    for cluster_id in label_coord:
        label_avg[cluster_id] = avg_list(label_coord[cluster_id])
        # print("Cluster " + str(cluster_id) + " avg: " + str(label_avg[cluster_id]))
        
    label_avg = dict(sorted(label_avg.items(), key=lambda item: item[1]))
    
    label_avg_lst = list(label_avg.keys())
    
    print(label_avg_lst)
    
    result = ''
    
    full_code = data["text"]
    
    for line in data["line_data"]:
        # tab_multiplier = 0
        if line["cluster_id"] in label_avg_lst:
            

            tab_multiplier = label_avg_lst.index(line["cluster_id"])
            
            # print("Tab Multiplier: " + str(tab_multiplier))
            
            text = line["text"]
            text = text.replace('\n', '')
            text = text.replace('\r', '')
            text = text.replace('\t', '')
            text = text.replace('\\', '')
            
            
            text = text.strip()
            
            #Updates the data on the line
            line["text"] = text
            
            # print("Particular Line Text")
            # print(text)
            # print((tab * tab_multiplier) + text + '\n')
            
            result += (tab * tab_multiplier) + text + '\n'
            
            # if len(data["line_data"]) > 15:
            #     print("Sleeping for 2 seconds, ebcause too many api calls might block the app")
            #     time.sleep(2)
            # time.sleep(2)
            
            
        
    # print("Resulting Text")
    # print(result)
    
    return result, data

def avg_list(lst):
    return sum(lst) / len(lst)


def final_processing(txt):
    
    print("Raw txt" + txt)
    
    raw_line_list = txt.split('\n')
    # print("raw_line_list: " + str(raw_line_list))
    
    txt = txt.strip()
    # print("stripped txt: " + txt)
    stripped_line_list = txt.split('\n')
    # print("stripped_line_list: " + str(stripped_line_list))
    
    # print("Raw list length" + str(len(raw_line_list)))
    # print("Stripped list length" + str(len(stripped_line_list)))
    
    return 0
    
    



@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def LM_correction_low(input_text, temperature=0.0):
    # print("Into the post process gpt function")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who helps correct OCR result of handwritten python code.",
        },
        {
            "role": "user",
            "content": f"""
Only fix typos in the following code. Do not change anything else. Here is the code:
{input_text}

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
        # print("trying GPT")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            # print("GPT worked")
            response_json = response.json()
            # print(response_json)
            result = response_json["choices"][0]["message"]["content"].strip()
            
        
            return result, response_json
        else:
            print("GPT failed")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""


@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def LM_correction_medium(input_text, temperature=0.0):
    # print("Into the post process gpt function")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who helps correct OCR result of handwritten python code.",
        },
        {
            "role": "user",
            "content": f"""
Fix typos in the following code. Make very minimum edits. Do not fix any logic. Here is the code: 
{input_text}

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
        # print("trying GPT")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            # print("GPT worked")
            response_json = response.json()
            # print(response_json)
            result = response_json["choices"][0]["message"]["content"].strip()
            
        
            return result, response_json
        else:
            print("GPT failed")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""


@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def LM_correction_high(input_text, temperature=0.0):
    # print("Into the post process gpt function")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who helps correct OCR result of handwritten python code.",
        },
        {
            "role": "user",
            "content": f"""
Fix every error in the following code. Here is the code:
{input_text}

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
        # print("trying GPT")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            # print("GPT worked")
            response_json = response.json()
            # print(response_json)
            result = response_json["choices"][0]["message"]["content"].strip()
            
        
            return result, response_json
        else:
            print("GPT failed")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def mathpix(image_path):
    result = None
    try:
        with open(image_path, "rb") as img_file:
            b64_image = base64.b64encode(img_file.read()).decode("utf-8")

        headers = {
            "app_id": MATHPIX_APP_ID,
            "app_key": MATHPIX_APP_KEY,
            "Content-type": "application/json",
        }

        data = {
            "src": "data:image/jpeg;base64," + b64_image,
            "formats": ["text"],
            "include_line_data": True
        }

        response = requests.post("https://api.mathpix.com/v3/text", headers=headers, json=data)
        response.raise_for_status()

        result = response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.ConnectionError as conn_err:
        print(f'Connection error occurred: {conn_err}')
    except FileNotFoundError:
        print(f'File {image_path} not found.')
    except Exception as err:
        print(f'An unexpected error occurred: {err}')
        
    return result


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
            
def total_clear_response(txt):

    first_tilda = txt.find("```")

    if first_tilda != -1:
        second_tilda = txt.find("```", first_tilda + 1)

        if second_tilda != -1:
            if txt[first_tilda + 3: first_tilda + 9] == "python" or txt[first_tilda + 3: first_tilda + 9] == "Python":
                return remove_blank_lines(remove_comments(txt[first_tilda + 9:second_tilda]))
            else:
                return remove_blank_lines(remove_comments(txt[first_tilda + 3:second_tilda]))
    
    return remove_blank_lines(remove_comments(txt))

def upload_image(image_path, filename):
    firebaseConfig = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
    "databaseURL": os.getenv('FIREBASE_DATABASE_URL'),
    "projectId": os.getenv('FIREBASE_PROJECT_ID'),
    "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    "appId": os.getenv('FIREBASE_APP_ID')
    }
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()

    cloud_path = "images/" + filename

        # Create a random token
    # token = str(uuid.uuid4())
    
    storage.child(cloud_path).put(image_path)

    # Get the URL of the uploaded image
    url = storage.child(cloud_path).get_url(None)
    
    print("URL: " + url)

    return url


# AWS OCR
@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def AWS_textract(file_path):
    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"The file {file_path} does not exist.")
        return

    # Create a Textract client
    try:
        client = boto3.client('textract')
    except Exception as e:
        print("Failed to create boto3 client.\n" + str(e))
        return

    # Open the image file
    try:
        with open(file_path, 'rb') as file:
            img = file.read()
            bytes_img = bytearray(img)
    except Exception as e:
        print("Failed to read file.\n" + str(e))
        return

    # Use Amazon Textract
    try:
        response = client.detect_document_text(Document={'Bytes': bytes_img})
    except Exception as e:
        print("Failed to process image with Textract.\n" + str(e))
        return

    # Check if 'Blocks' in response
    if 'Blocks' in response:
        # Print detected text
        lines = [item.get('Text') for item in response["Blocks"] if item["BlockType"] == "LINE"]
        if lines:
            result = ''
            for i in range(len(lines)):
                if i != 0:
                    result += '\n' + lines[i]
                else:
                    result += lines[i]
            return result
        else:
            print("No text detected.")
    else:
        print("No blocks in the response from Textract.")


# Azure OCR
@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def azure(image_path):
    
    # Open the image
    with open(image_path, "rb") as image_stream:
        image_analysis = AZURE_computervision_client.read_in_stream(image_stream, raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    operation_location = image_analysis.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        results = AZURE_computervision_client.get_read_result(operation_id)
        if results.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    # Print results, line by line
    result = ''
    if results.status == OperationStatusCodes.succeeded:
        for text_result in results.analyze_result.read_results:
            for i in range(len(text_result.lines)):
                if i != 0:
                    result += '\n' + text_result.lines[i].text
                else:
                    result += text_result.lines[i].text


    return result



# GCV OCR


@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def GCV(image_path):
    with open(image_path, "rb") as img_file:
        file_content = img_file.read()
    GCV_image = vision.Image(content=file_content)
    GCV_response = gcloud_vision_client.document_text_detection(image=GCV_image)

    GCV_response_text = GCV_response.full_text_annotation.text
    
    return GCV_response_text



    
    
    

@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def LM_correction_low_chris(input_text, temperature=0.0):
    # print("Into the post process gpt function")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who helps correct OCR result of handwritten python code.",
        },
        {
            "role": "user",
            "content": f'''
A student intro program who is working on an assignment. We have a scan of their code, but it is not quite right. We need you to fix the scan so that it captures what the student wrote.
Fix the scan, which might have some small typographic errors. For example here is a scan and its corrected version:

Scan:
# A pnogsam to check if a numbar is prlme.
dof is -prime (n):
110V
Returns True if n is prime, False otherwise.
11011
if n <= 1:
return False
for i in range (2 , int(n**0.5 ) +1): :
if n % i == 0 :
return False
return True
def main():
The main function.
n= int (input ( "Enter a number: ")
if is-prime (n):
print ( n , "is a prime number.")
else :
print( n, "is not a prime number. ")
if
name
11
main
",
"
;
main()

Correct version:
# A program to check if a number is prime.
def is_prime(n):
    """
    Returns True if n is prime, False otherwise.
    """
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def main():
    """
    The main function.
    """
    n = int(input("Enter a number: "))
    if is_prime(n):
        print(n, "is a prime number.")
    else:
        print(n, "is not a prime number.")


if __name__ == "__main__":
    main()


Here is the student scan that you need to fix:
{input_text}


Important! Do not add anything to your result by yourself that is not in the code(Including Comments). You should absolutely never give away the solution to the assignment! Instead you should faithfully preserve the code that the student has written.

Return the result in the below format:
```python
code goes here
```
''',
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
    
    
#New cleaning


'''
This function removes comments from the code
Limitation: - Would also delete strings if they have # in them
            - Would also delete strings with """in them"""
'''


def remove_comments(code):
    lines = code.split("\n")
    cleaned_code = ""
    in_multiline_comment = False
    for line in lines:
        if '"""' in line:
            if in_multiline_comment:
                in_multiline_comment = False
                continue
            else:
                in_multiline_comment = True
        if in_multiline_comment:
            continue

        comment_index = line.find('#')
        if comment_index != -1:
            # Extract the code part
            clean_line = line[:comment_index]
            if clean_line.strip() != "":
                cleaned_code += clean_line + "\n"
        else:
            cleaned_code += line + "\n"
    return cleaned_code


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

def fmt_code(code: str) -> str:
    try:
        return black.format_str(code, mode=black.FileMode())

    except InvalidInput as e:
        print(f"Invalid Python code: {e}")
        print(f"Code: {code}")
        return code

    except Exception as e:
        print(f"Unexpected error with Black auto-styling: {e}")
        print(f"Code: {code}")
        return code
    
    
    
# result = remove_comments(test_str)
# result = remove_blank_lines(result)
# result = normalize_indentation(result)

# print(result)


def lm_eachline(input_text):
    print("into the line by line function")
    lines = input_text.split("\n")
    result = ""
    for line in lines:
        result += total_clear_response(str(LM_line(line, input_text)))
        time.sleep(2)
    
    return result
        
# LM Function for line by line application. 
@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def LM_line(line, entire_code, temperature=0.0):
    # print("Into the post process gpt function")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who helps correct OCR result of handwritten python code.",
        },
        {
            "role": "user",
            "content": f"""
Here is the output from the OCR:
{entire_code}

please only return the corrected version of the single following line of code
{line}

Rules of correcting:
1. Do not fix any kind of logic by yourself, if there is something wrong in the code let it be.
2. Do not add anything that by yourself, just correct typos in the code.

return code in the following format:
```python
single line of code goes here.
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



# Double prompting function

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




"""
Payload Deliverable Function
"""

# Double prompting function

@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def initial_prompt_payload(entire_code, temperature=0.0):
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
Only correct all spelling mistakes in the code.


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
            
        
            return result, payload, response_json
        else:
            print("GPT failed")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""



@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def double_prompt_payload(entire_code, temperature=0.0):
    # print("Into the post process gpt function")
    initial_LM_code, initial_payload, initial_response_json = initial_prompt_payload(entire_code)
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
Only correct all spelling mistakes in the code.


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
            
        
            return initial_payload, initial_response_json, payload, response_json
        else:
            print("GPT failed")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""


@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def simple_prompt(input_text, temperature=0.0):
    # print("Into the post process gpt function")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who helps correct OCR result of handwritten python code.",
        },
        {
            "role": "user",
            "content": f"""
Only fix typos in the following code. Do not change anything else. Here is the code:
{input_text}

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
        # print("trying GPT")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            # print("GPT worked")
            response_json = response.json()
            # print(response_json)
            result = response_json["choices"][0]["message"]["content"].strip()
            
        
            return payload, response_json
            # return result
        else:
            print("GPT failed")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""




@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def GCV_payload(path):
    # Load the service account key file
    creds = service_account.Credentials.from_service_account_file(gcloud_key_path)
    if creds.requires_scopes:
        creds = creds.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])

    # Get an access token
    auth_req = Request()
    creds.refresh(auth_req)
    access_token = creds.token

    with open(path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    url = 'https://vision.googleapis.com/v1/images:annotate'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token),  # Use the access token
    }
    data = {
        'requests': [{
            'image': {
                'content': encoded_string,
            },
            'features': [{
                'type': 'DOCUMENT_TEXT_DETECTION',
            }],
        }],
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code != 200:
        raise Exception(
            "Request failed with status code {}. Message: {}".format(response.status_code, response.json()['error']['message'])
        )

    return response.json()

    
    
# AWS OCR
@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def AWS_textract_payload(file_path):
    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"The file {file_path} does not exist.")
        return

    # Create a Textract client
    try:
        client = boto3.client('textract')
    except Exception as e:
        print("Failed to create boto3 client.\n" + str(e))
        return

    # Open the image file
    try:
        with open(file_path, 'rb') as file:
            img = file.read()
            bytes_img = bytearray(img)
    except Exception as e:
        print("Failed to read file.\n" + str(e))
        return

    # Use Amazon Textract
    try:
        response = client.detect_document_text(Document={'Bytes': bytes_img})
        return response
    except Exception as e:
        print("Failed to process image with Textract.\n" + str(e))
        return
        

"""
# Azure OCR
@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def azure_payload(image_path):
    
    # Open the image
    with open(image_path, "rb") as image_stream:
        image_analysis = AZURE_computervision_client.read_in_stream(image_stream, raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    operation_location = image_analysis.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        results = AZURE_computervision_client.get_read_result(operation_id)
        if results.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    if results.status == OperationStatusCodes.succeeded:
        return results"""
        

# class AzureEncoder(json.JSONEncoder):
#     def default(self, o):
#         return o.__dict__
    
@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def azure_payload(image_path):
    
    # Set the API endpoint
    analyze_url = AZURE_ENDPOINT + "computervision/imageanalysis:analyze?api-version=2023-02-01-preview&features=read"

    # Open the image file
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        
    # Set the headers
    headers = {"Ocp-Apim-Subscription-Key": AZURE_KEY, 
                "Content-Type": "application/octet-stream"}
    
    # Make the request
    response = requests.post(analyze_url, headers=headers, data=image_data)
    
    # If the request was successful, the status code will be 200
    if response.status_code == 200:
        return response.json()
    else:
        return "Error: " + response.text

@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, Exception), max_tries=10, on_backoff=backoff_hdlr)
def mathpix_payload(image_path):
    result = None
    try:
        with open(image_path, "rb") as img_file:
            b64_image = base64.b64encode(img_file.read()).decode("utf-8")

        headers = {
            "app_id": MATHPIX_APP_ID,
            "app_key": MATHPIX_APP_KEY,
            "Content-type": "application/json",
        }

        data = {
            "src": "data:image/jpeg;base64," + b64_image,
            "formats": ["text"],
            "include_line_data": True
        }

        response = requests.post("https://api.mathpix.com/v3/text", headers=headers, json=data)
        response.raise_for_status()

        result = response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.ConnectionError as conn_err:
        print(f'Connection error occurred: {conn_err}')
    except FileNotFoundError:
        print(f'File {image_path} not found.')
    except Exception as err:
        print(f'An unexpected error occurred: {err}')
        
    return result
    

# Only works for microsoft azure as of now. 
def line_data(raw_api_datum):
    extracted_api_data = {
        "ocr_ouptut": []
    }

    for i, line in enumerate(raw_api_datum["readResult"]['pages'][0]['lines']):
        line_dict = {}
        coords_list = line['boundingBox']
        # Quadrangle bounding box of a line or word, depending on the parent object, specified as a list of 8 numbers. The coordinates are specified relative to the top-left of the original image. The eight numbers represent the four points, clockwise from the top-left corner relative to the text orientation. For image, the (x, y) coordinates are measured in pixels. For PDF, the (x, y) coordinates are measured in inches.
        (
            tl_x, tl_y,
            tr_x, tr_y,
            br_x, br_y,
            bl_x, bl_y 
        ) = coords_list
        
        x_coord = coords_list[0]
        y_coord = coords_list[1]
        line_dict['x'] = x_coord
        line_dict['y'] = y_coord
        line_dict['w'] = tr_x - tl_x
        line_dict['h'] = bl_y - tl_y
        line_dict['line_num'] = i+1
        line_dict['text'] = line['content'].strip()        
        
        extracted_api_data["ocr_ouptut"].append(line_dict)

    return extracted_api_data
    
    
