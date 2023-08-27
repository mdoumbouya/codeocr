from sklearn.cluster import MeanShift, estimate_bandwidth
import numpy as np
import json
import matplotlib.pyplot as plt
import cv2
import requests
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


load_dotenv()

MATHPIX_APP_ID = os.getenv("MATHPIX_APP_ID")
MATHPIX_APP_KEY = os.getenv("MATHPIX_APP_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
GPT_MODEL = "gpt-4-0613"




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
    
    print(type(labels))
    print(len(data["line_data"]))
    
    print("Mathpix data:")
    for elem in data:
        print(elem)
        print(type(data[elem]))
        
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
    
    

# Will use it when necessary. 
def LM_correction_low(input_text):
    print("Into the post process gpt function")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who helps translate OCR result of handwritten python code from Mathpix API to Python code.",
        },
        {
            "role": "user",
            "content": f"""Only fix typos in the following code. Do not change anything else.
            Here is the code{input_text}
            
            return your result in the below form

            ```Python
            result
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
    }

    try:
        print("trying GPT")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("GPT worked")
            response_json = response.json()
            # print(response_json)
            result = response_json["choices"][0]["message"]["content"].strip()
            
            print("Gpt data types")
            for elem in response_json:
                print(type(response_json[elem]))
        
            return result, response_json
        else:
            print("GPT failed")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""


def LM_correction_medium(input_text):
    print("Into the post process gpt function")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who helps translate OCR result of handwritten python code from Mathpix API to Python code.",
        },
        {
            "role": "user",
            "content": f"""fix typos in the following code. Make very minimum edits. Do not fix any logic.
            Here is the code{input_text}
            
            return your result in the below form

            ```Python
            result
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
    }

    try:
        print("trying GPT")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("GPT worked")
            response_json = response.json()
            # print(response_json)
            result = response_json["choices"][0]["message"]["content"].strip()
            
            print("Gpt data types")
            for elem in response_json:
                print(type(response_json[elem]))
        
            return result, response_json
        else:
            print("GPT failed")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""
    
def LM_correction_high(input_text):
    print("Into the post process gpt function")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who helps translate OCR result of handwritten python code from Mathpix API to Python code.",
        },
        {
            "role": "user",
            "content": f"""Fix every error in the following code.
            Here is the code{input_text}
            
            return your result in the below form

            ```Python
            result
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
    }

    try:
        print("trying GPT")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("GPT worked")
            response_json = response.json()
            # print(response_json)
            result = response_json["choices"][0]["message"]["content"].strip()
            
            print("Gpt data types")
            for elem in response_json:
                print(type(response_json[elem]))
        
            return result, response_json
        else:
            print("GPT failed")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""


def mathpix(image_path):
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

        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return None

def clear_response(txt):

    first_tilda = txt.find("```")

    if first_tilda != -1:
        second_tilda = txt.find("```", first_tilda + 1)

        if second_tilda != -1:
            if txt[first_tilda + 3: first_tilda + 9] == "python" or txt[first_tilda + 3: first_tilda + 9] == "Python":
                return txt[first_tilda + 9:second_tilda]
            else:
                return txt[first_tilda + 3:second_tilda]
            
            

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



    