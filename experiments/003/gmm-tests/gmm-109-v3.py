import matplotlib.pyplot as plt
import json
from sklearn.mixture import GaussianMixture
import numpy as np
import argparse
import copy
import editdistance
from scipy.stats import norm
import cv2
import plotly.graph_objects as go

INDENTATION = '    '

def visualize_all(data, deltas):
    """
    Visualizes both indentation factors and deltas for each line of code.

    Parameters:
    data (list of dicts): Contains code line information with line number and indentation factor.
    deltas (list): A list of delta values for each line.
    """
    # Extracting line numbers, indentation factors, and deltas
    line_numbers = [item['line_num'] for item in data]
    indentation_factors = [item['indentation_factor'] for item in data]

    # Creating a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # Plotting deltas
    colors = ['green' if delta > 0 else 'red' for delta in deltas]
    ax1.bar(line_numbers[1:], deltas, color=colors)
    ax1.set_title('Delta X by Line Number')
    ax1.set_xlabel('Line Number')
    ax1.set_ylabel('Delta X')
    
    # Plotting indentation factors
    ax2.barh(line_numbers, indentation_factors, color='blue')
    ax2.set_title('Indentation Factor by Line Number')
    ax2.set_xlabel('Line Number')
    ax2.set_ylabel('Indentation Factor')
    ax2.invert_yaxis()
    ax2.grid(True)

    

    # Displaying the figure
    plt.tight_layout()
    plt.show()

import plotly.graph_objects as go

def visualize_indentation_plotly(data):
    """
    Visualizes the indentation factors using Plotly with horizontal bars.

    Parameters:
    data (list of dicts): Contains code line information with line number and indentation factor.
    """
    # Extracting line numbers and indentation factors
    line_numbers = [item['line_num'] for item in data]
    indentation_factors = [item['indentation_factor'] for item in data]

    # Plotting with Plotly
    fig = go.Figure(data=[go.Bar(x=indentation_factors, y=line_numbers, orientation='h')])
    fig.update_layout(
        title='Indentation Factor by Line Number',
        xaxis_title='Indentation Factor',
        yaxis_title='Line Number',
        template='plotly_white'  # You can choose other templates
    )
    fig.update_yaxes(autorange="reversed")  # For reversed y-axis
    fig.show()


def visualize_deltas_plotly(data_points, deltas):
    """
    Visualizes the deltas using Plotly with vertical bars.

    Parameters:
    data_points (list): List of dictionaries representing data points with 'line_num'.
    deltas (list): List of delta values corresponding to data points.
    """
    line_nums = [point['line_num'] for point in data_points][1:]
    colors = ['green' if delta > 0 else 'red' for delta in deltas]

    # Plotting with Plotly
    fig = go.Figure(data=[go.Bar(x=line_nums, y=deltas, marker_color=colors)])
    fig.update_layout(
        title='Delta X by Line Number',
        xaxis_title='Line Number',
        yaxis_title='Delta X',
        template='plotly_white'  # You can choose other templates
    )
    fig.show()

def annotate_deltas(data_points, deltas):
  """
  This function annotates the data points with their corresponding delta values and delta types.

  Parameters:
  data_points (list): A list of dictionaries where each dictionary represents a data point.
  deltas (list): A list of delta values. The length of this list should be equal to the number 
                  of data points minus one.

  Returns:
  list: Returns a list of modified data points with added 'delta' and 'delta_type' keys. The 
        'delta' key will have the corresponding value from deltas list. The 'delta_type' key 
        will have 'positive' if the delta is greater than 0, 'negative' if the delta is less 
        than 0, and None if the delta is 0 or for the first data point.
  """
  modified_data_points = copy.deepcopy(data_points)
  for i, point in enumerate(modified_data_points):
    if i != 0:
      point['delta'] = deltas[i-1]
      if deltas[i-1] > 0:
        point['delta_type'] = 'positive'
      elif deltas[i-1] < 0:
        point['delta_type'] = 'negative'
      else:
        point['delta_type'] = 'null'
    else:
      point['delta'] = None
      point['delta_type'] = None
  
  return modified_data_points

def add_gmm_prediction_labels(data_points, gmm_prediction):
  """
  This function adds Gaussian Mixture Model (GMM) prediction labels to the data points.
  
  Parameters:
  data_points (list): A list of dictionaries where each dictionary represents a data point. 
                      Each data point must have a 'delta_type' key.
  gmm_prediction (list): A list of GMM predictions. The length of this list should be equal to 
                          the number of 'positive' delta_type in data_points.
  
  Returns:
  list: Returns a list of modified data points with added 'gmm_prediction' key. If 'delta_type' 
        is 'positive', 'gmm_prediction' key will have the corresponding value from gmm_prediction 
        list. If 'delta_type' is not 'positive', 'gmm_prediction' key will have None as value.
  """
  modified_data_points = copy.deepcopy(data_points)
  i = 0
  for point in modified_data_points:
    if point['delta_type'] == 'positive':
      point['gmm_prediction'] = str(gmm_prediction[i])
      i += 1
    else:
      point['gmm_prediction'] = None
  return modified_data_points
  

# Indentation Type compared to last line
# Indentation Factor compared to last line
def process_gmm_prediction(data_points):
  """
  This function processes the Gaussian Mixture Model (GMM) prediction labels of the data points 
  and determines the labels for increment and neutral deltas.

  Parameters:
  data_points (list): A list of dictionaries where each dictionary represents a data point. 
                      Each data point must have 'delta', 'delta_type', and 'gmm_prediction' keys.

  Returns:
  tuple: Returns a tuple of two strings. The first string is the label for increment deltas 
          (deltas that are greater than 0) and the second string is the label for neutral deltas 
          (deltas that are equal to 0). The labels are determined based on the mean of the deltas 
          for each label. The label with the higher mean is considered as the increment label.
  """
  ids_dict = {}
  for data in data_points:
    if data['delta_type'] == 'positive':
      label = data['gmm_prediction']
      str_label = str(label)
      if str_label not in ids_dict:
        ids_dict[str_label ] = []
      ids_dict[str_label].append(data['delta'])
      
  ids_dict['0'] = np.mean(ids_dict['0'])
  ids_dict['1'] = np.mean(ids_dict['1'])
  
  if ids_dict['0'] > ids_dict['1']:
    increment_label = '0'
    neutral_label = '1'
  else:
    increment_label = '1'
    neutral_label = '0'
  
  return increment_label, neutral_label
  

def custom_get_gmm_prediction(data_points, image_id):
  """
  This function performs Gaussian Mixture Model (GMM) prediction on the 'delta' values of the 
  data points where 'delta_type' is 'positive'.

  Parameters:
  data_points (list): A list of dictionaries where each dictionary represents a data point. 
                      Each data point must have 'delta' and 'delta_type' keys.

  Returns:
  numpy.ndarray: Returns an array of GMM predictions for the 'delta' values of the data points 
                  where 'delta_type' is 'positive'. The length of this array is equal to the 
                  number of 'positive' delta_type in data_points.
  """
  positive_list = []
  for data in data_points:
    if data['delta_type'] == 'positive':
      positive_list.append(data['delta'])
  
  neautral_mean = 0.0072602999579008815 
  neutral_var = 2.6859744231825193e-05
  neutral_std = 0.008279078889046027

  increment_mean = 0.0777810811891604 
  increment_var = 0.0006160921671065933
  increment_std = 0.024844347044055918
  
  neutral_gaussian = norm(loc=neautral_mean, scale=neutral_std)
  increment_gaussian = norm(loc=increment_mean, scale=increment_std)
  
  image_path = f'../images/{image_id}.jpg'
  image_width = cv2.imread(image_path).shape[1]
  
  gmm_prediction = []
  for data in positive_list:
    data = data / image_width
    if neutral_gaussian.pdf(data) > increment_gaussian.pdf(data):
      gmm_prediction.append(0)
    else:
      gmm_prediction.append(1)
  
  return gmm_prediction

def print_data_points(data_points):
  for point in data_points:
    print(f"{point}")



def find_cluster_mean(data_points, line_num):
  print("Target line:")
  print(data_points[line_num - 1])
  print("\n")
  print("Previous lines:")
  distance_dict = {}
  for i in range(line_num - 2, -1, -1):
    if data_points[i]['indentation_factor'] not in distance_dict:
      distance_dict[data_points[i]['indentation_factor']] = []
    distance_dict[data_points[i]['indentation_factor']].append(abs(data_points[i]['x'] - data_points[line_num - 1]['x']))
  
  # print(distance_dict)
  for key in distance_dict:
    distance_dict[key] = np.mean(distance_dict[key])
  print(distance_dict)
  # Now we will sort the dictionary on the basis of the values in ascending order
  sorted_distance_dict = {k: v for k, v in sorted(distance_dict.items(), key=lambda item: item[1])}
  
  print("Cluster Mean:")
  print(sorted_distance_dict)
  # Now we will print the first element of the sorted dictionary
  # print("The first element of the sorted dictionary is:")
  # print(list(sorted_distance_dict.keys())[0])
  # print("\n")
  return list(sorted_distance_dict.keys())[0]


def find_cluster_nearest_neighbour(data_points, line_num):
  # print("Target line:")
  # print(data_points[line_num - 1])
  
  distance_dict = {}
  for i in range(line_num - 2, -1, -1):
    if data_points[i]['indentation_factor'] not in distance_dict:
      distance_dict[data_points[i]['indentation_factor']] = []
      distance_dict[data_points[i]['indentation_factor']].append(abs(data_points[i]['x'] - data_points[line_num - 1]['x']))
  
  # print("Previous lines:")
  # print(distance_dict)
  
  sorted_distance_dict = {k: v for k, v in sorted(distance_dict.items(), key=lambda item: item[1])}
  
  # print("sorted Nearest Neighobours:")
  # print(sorted_distance_dict)
  # Now we will print the first element of the sorted dictionary
  # print("The first element of the sorted dictionary is:")
  # print(list(sorted_distance_dict.keys())[0])
  # print("\n")
  return list(sorted_distance_dict.keys())[0]


def create_code(data_points):
  result = ''
  for data in data_points:
      result += f"{INDENTATION * data['indentation_factor']}{data['text']}\n"
      
  return result
  

# Draw it all on goodnotes 109project notebook
def process_indentation(data_points, increment_label, neutral_label):
  modified_data_points = copy.deepcopy(data_points)
  
  for i in range(len(modified_data_points)):
    modified_data_points[i]['indentation_factor'] = 0
  
  for i in range(len(modified_data_points)):
    if i != 0:
      
      if modified_data_points[i]['delta_type'] == 'positive':
        if modified_data_points[i]['gmm_prediction'] == increment_label:
          modified_data_points[i]['indentation_factor'] = modified_data_points[i - 1]['indentation_factor'] + 1
          
        elif modified_data_points[i]['gmm_prediction'] == neutral_label:
          modified_data_points[i]['indentation_factor'] = modified_data_points[i - 1]['indentation_factor']
          
      elif modified_data_points[i]['delta_type'] == 'negative':
        # cluster_mean = find_cluster_mean(modified_data_points, i + 1)
        cluster_nn = find_cluster_nearest_neighbour(modified_data_points, i + 1)
        # print(f"cluster_mean: {cluster_mean}")
        # print(f"cluster_nn: {cluster_nn}")
        modified_data_points[i]['indentation_factor'] = cluster_nn
      
      elif modified_data_points[i]['delta_type'] == 'null':
        modified_data_points[i]['indentation_factor'] = modified_data_points[i - 1]['indentation_factor']
    else:
      modified_data_points[i]['indentation_factor'] = 0
  
  
  return modified_data_points




def main(args):
  IMAGE_ID = int(args.image_id)

  with open('output/postprocessed_ocr_provider_data.json') as f:
      data = json.load(f)

  data_points = data[IMAGE_ID]['ocr_ouptut']

  # get all x's into a list
  x_coordinates = [point['x'] for point in data_points]
  deltas = [x_coordinates[n] - x_coordinates[n - 1] for n in range(1, len(x_coordinates))]

  modified_data_points = annotate_deltas(data_points, deltas)
  #print(f"modified_data_points, after annotated deltas:\n {modified_data_points}")
  
  gmm_prediction = custom_get_gmm_prediction(modified_data_points, IMAGE_ID)
  print(f"gmm_prediction:\n {gmm_prediction}")
  
  modified_data_points = add_gmm_prediction_labels(modified_data_points, gmm_prediction) # For delta type positive adds GMM Label, for {negative, null, and and none} adds None to GMM Prediction Lable
  increment_label, neutral_label = '1', '0'
  # print_data_points(modified_data_points)
  
  
  modified_data_points = process_indentation(modified_data_points, increment_label, neutral_label)
  
  print("\n\n")
  code = create_code(modified_data_points)
  print(f"{code}")
  
  if args.visualize == 'true':
    visualize_deltas_plotly(modified_data_points, deltas)
    visualize_indentation_plotly(modified_data_points)
    # visualize_all(modified_data_points, deltas)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-id", required=True, help="Give the image ID")
    parser.add_argument("--visualize", help="Optional argument for visualizing the delta X values for each line in a graph")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
    
    