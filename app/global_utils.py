from sklearn.cluster import MeanShift, estimate_bandwidth
import numpy as np
import json
import matplotlib.pyplot as plt
import cv2
import requests
import base64
import io

# Clustering functions
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from google.cloud import vision_v1

def detect_lines(response):
    x_values = []
    y_values = []

    # Get the text_annotations from the response object
    text_annotations = response.text_annotations

    # Loop through each text annotation
    for annotation in text_annotations:
        vertices = annotation.bounding_poly.vertices

        # Loop through each vertex
        for vertex in vertices:
            x_values.append(vertex.x)
        y_values.append((vertices[0].y + vertices[3].y) / 2)  # Taking average of y-coordinates of first and third vertex

    # Convert y_values to numpy array and reshape for sklearn
    y_values_np = np.array(y_values).reshape(-1, 1)

    # Estimate the optimal bandwidth
    # bandwidth = estimate_bandwidth(y_values_np, quantile=0.05)  You can adjust the quantile parameter based on your data

    # Define the Mean Shift model with the estimated bandwidth
    mean_shift = MeanShift(bandwidth=20)

    # Fit the model
    mean_shift.fit(y_values_np)

    # Get cluster centers
    cluster_centers = mean_shift.cluster_centers_

    # Get labels for each point
    labels = mean_shift.labels_

    # Create a new dictionary to store the line_id values
    line_ids = {}
    for ix, line_id in enumerate(labels):
        line_ids[ix] = line_id  # Use the index as the key

    return response, line_ids  # Return both the response object and the line_ids dictionary
  
  

def annotate_image(image_path, response):
    response, line_ids = detect_lines(response)  # Receive both the response object and the line_ids dictionary

    # Load the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Draw bounding boxes around entire lines
    # Get the text_annotations from the response object
    text_annotations = response.text_annotations

    # Loop through each text annotation
    for ix, annotation in enumerate(text_annotations):
        vertices = annotation.bounding_poly.vertices
        line_id = line_ids[ix]  # Get the line_id from the line_ids dictionary using the index
        line_color = LINE_COLORS[line_id % len(LINE_COLORS)]

        # Create an array of points for the bounding box
        pts = np.array([[vertex.x, vertex.y] for vertex in vertices[0:2]], np.int32)  # Use dot notation to access x and y properties
        pts = pts.reshape((-1,1,2))

        # Draw the bounding box on the image
        cv2.polylines(image, [pts], True, line_color, 3)

    # Save the image with bounding boxes
    is_success, im_buf_arr = cv2.imencode(".jpg", image)
    byte_im = im_buf_arr.tobytes()
    img_str = base64.b64encode(byte_im).decode('utf-8')

    return img_str



LINE_COLORS = [
    (255, 0, 0),       # red
    (255, 128, 0),     # orange
    (255, 255, 0),     # yellow
    (128, 255, 0),     # lime
    (0, 255, 0),       # green
    (0, 255, 128),     # spring green
    (0, 255, 255),     # cyan
    (0, 128, 255),     # azure
    (0, 0, 255),       # blue
    (128, 0, 255),     # violet
    (255, 0, 255),     # magenta
    (255, 0, 128),     # rose
    (255, 64, 0),      # tangerine
    (255, 192, 0),     # golden yellow
    (192, 255, 0),     # spring lime
    (0, 255, 64),      # bright green
    (0, 255, 192),     # mint green
    (0, 192, 255),     # bright azure
    (0, 64, 255),      # sky blue
    (64, 0, 255),      # indigo
    (255, 0, 64),      # deep pink
    (255, 128, 128),   # coral
    (255, 255, 128),   # pastel yellow
    (128, 255, 128),   # pastel green
    (128, 255, 255),   # pastel cyan
    (128, 128, 255),   # pastel blue
    (255, 128, 255),   # pastel magenta
    (255, 64, 128),    # salmon
    (255, 192, 128),   # peach
    (192, 255, 128)    # honeydew
]
