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
    