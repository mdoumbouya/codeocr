# Super Important

from sklearn.cluster import MeanShift
import numpy as np
import json

import matplotlib.pyplot as plt

def detect_lines(response):
    x_values = []
    y_values = []

    # Loop through each text annotation
    for annotation in response['responses'][0]['textAnnotations']:
      vertices = annotation['boundingPoly']['vertices']
      
      # Loop through each vertex
      for vertex in vertices:
        x_values.append(vertex['x'])
      y_values.append((vertices[0]['y'] + vertices[3]['y']) / 2)  # Taking average of y-coordinates of first and third vertex



    # Convert y_values to numpy array and reshape for sklearn
    y_values_np = np.array(y_values).reshape(-1, 1)

    # Define the Mean Shift model
    mean_shift = MeanShift(bandwidth=10)  # Bandwidth is a parameter of the Mean shift algorithm, you may need to adjust this based on your data

    # Fit the model
    mean_shift.fit(y_values_np)

    # Get cluster centers
    cluster_centers = mean_shift.cluster_centers_

    # Get labels for each point
    labels = mean_shift.labels_
    for ix, line_id in enumerate(labels):
      response['responses'][0]['textAnnotations'][ix]['line_id'] = line_id

    return response