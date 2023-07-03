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

load_dotenv()

MATHPIX_APP_ID = os.getenv("MATHPIX_APP_ID")
MATHPIX_APP_KEY = os.getenv("MATHPIX_APP_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

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
    
    print(len(labels))
    print(len(data["line_data"]))
        
    for i, line in enumerate(data["line_data"]):
        line["cluster_id"] = labels[i]
        
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
        print("Cluster " + str(cluster_id) + " avg: " + str(label_avg[cluster_id]))
        
    label_avg = dict(sorted(label_avg.items(), key=lambda item: item[1]))
    
    label_avg_lst = list(label_avg.keys())
    
    print(label_avg_lst)
    
    result = ''
    
    full_code = data["text"]
    
    for line in data["line_data"]:
        # tab_multiplier = 0
        if line["cluster_id"] in label_avg_lst:
            

            tab_multiplier = label_avg_lst.index(line["cluster_id"])
            
            print("Tab Multiplier: " + str(tab_multiplier))
            
            text = line["text"]
            text = text.replace('\n', '')
            text = text.replace('\r', '')
            text = text.replace('\t', '')
            text = text.replace('\\', '')
            
            text = LM_correction(full_code, text)
            
            text = clear_response(text)
            
            line["text"] = text
            
            text = text.strip()
            
            print("Particular Line Text")
            print(text)
            print((tab * tab_multiplier) + text + '\n')
            
            result += (tab * tab_multiplier) + text + '\n'
            
            time.sleep(2)
            
            
        
    print("Resulting Text")
    print(result)
    
    return result, data

def avg_list(lst):
    return sum(lst) / len(lst)


def final_processing(txt):
    
    print("Raw txt" + txt)
    
    raw_line_list = txt.split('\n')
    print("raw_line_list: " + str(raw_line_list))
    
    txt = txt.strip()
    print("stripped txt: " + txt)
    stripped_line_list = txt.split('\n')
    print("stripped_line_list: " + str(stripped_line_list))
    
    print("Raw list length" + str(len(raw_line_list)))
    print("Stripped list length" + str(len(stripped_line_list)))
    
    return 0
    
    
    
def LM_correction(full_code, line):
    print("Into the post process gpt function")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who helps translate result of handwritten python code from Mathpix API to Python code.",
        },
        {
            "role": "user",
            "content": f"""here is the whole code for context but dont use it for anything else
                        {full_code}
                        
                        Here is a line from the output of Mathpix API, it can be either plain text, code, or a comment. Different rule applies for different situaiton.  
                        {line} 
                        
                        Some instructions
                        if it's just a plain line of text, then return just the text with corrections in spelling or some mistake that an ocr might make. 
                        
                        if it's code
                        1. Fix all sorts of typos in the line of code, including the string; 
                        2.  "return exactly the same number of lines as the input, including comments in Python code, and do not change the order of the lines or increase the number of lines."
                        3. A post-processing code already corrected the indentation of each line. Do not do anything about the indentation. Just work like a word correction model. 
                        4. return nothing but the corrected line of code
                        
                        In any case, whatever you return, return it in the below format.
                        
                        ```python
                        particular line
                        ```
                        
                        Make sure you are follow every rule very strictly.
                        """
        },
    ]

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    payload = {
        "model": "gpt-4-0613",
        "messages": messages,
        "max_tokens": 2042,
    }

    try:
        print("trying GPT")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("GPT worked")
            response_json = response.json()
            result = response_json["choices"][0]["message"]["content"].strip()
            return result
        else:
            print("GPT failed")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""


def clear_response(txt):

    first_tilda = txt.find("```")

    if first_tilda != -1:
        second_tilda = txt.find("```", first_tilda + 1)

        if second_tilda != -1:
            if txt[first_tilda + 3: first_tilda + 9] == "python" or txt[first_tilda + 3: first_tilda + 9] == "Python":
                return txt[first_tilda + 9:second_tilda]
            else:
                return txt[first_tilda + 3:second_tilda]

    