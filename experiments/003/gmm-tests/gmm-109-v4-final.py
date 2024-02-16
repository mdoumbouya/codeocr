import matplotlib.pyplot as plt
import json
from sklearn.mixture import GaussianMixture
import numpy as np
import argparse
import copy
import editdistance
from scipy.stats import norm
import cv2
from code_ocr.indentation_recognition import GaussianIndentationRecognitionAlgo
from code_ocr.post_correction import SIMPLEprompting_test3

INDENTATION = '    '

# Added to the code
def annotate_deltas(lines, deltas):
  """
  This function annotates the data points with their corresponding delta values and delta types.

  Parameters:
  lines (list): A list of dictionaries where each dictionary represents a data point.
  deltas (list): A list of delta values. The length of this list should be equal to the number 
                  of data points minus one.

  Returns:
  list: Returns a list of modified data points with added 'delta' and 'delta_type' keys. The 
        'delta' key will have the corresponding value from deltas list. The 'delta_type' key 
        will have 'positive' if the delta is greater than 0, 'negative' if the delta is less 
        than 0, and None if the delta is 0 or for the first data point.
  """
  modified_lines = copy.deepcopy(lines)
  for i, point in enumerate(modified_lines):
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
  
  return modified_lines

def add_gaussian_prediction_labels(lines, gaussian_prediction):
  """
  This function adds Gaussian Mixture Model (gaussian) prediction labels to the data points.
  
  Parameters:
  lines (list): A list of dictionaries where each dictionary represents a data point. 
                      Each data point must have a 'delta_type' key.
  gaussian_prediction (list): A list of gaussian predictions. The length of this list should be equal to 
                          the number of 'positive' delta_type in lines.
  
  Returns:
  list: Returns a list of modified data points with added 'gaussian_prediction' key. If 'delta_type' 
        is 'positive', 'gaussian_prediction' key will have the corresponding value from gaussian_prediction 
        list. If 'delta_type' is not 'positive', 'gaussian_prediction' key will have None as value.
  """
  modified_lines = copy.deepcopy(lines)
  i = 0
  for point in modified_lines:
    if point['delta_type'] == 'positive':
      point['gaussian_prediction'] = str(gaussian_prediction[i])
      i += 1
    else:
      point['gaussian_prediction'] = None
  return modified_lines
  

def get_gaussian_prediction(lines, image_id):
  """
  This function performs Gaussian Mixture Model (gaussian) prediction on the 'delta' values of the 
  data points where 'delta_type' is 'positive'.

  Parameters:
  lines (list): A list of dictionaries where each dictionary represents a data point. 
                      Each data point must have 'delta' and 'delta_type' keys.

  Returns:
  numpy.ndarray: Returns an array of gaussian predictions for the 'delta' values of the data points 
                  where 'delta_type' is 'positive'. The length of this array is equal to the 
                  number of 'positive' delta_type in lines.
  """
  positive_list = []
  for data in lines:
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
  
  gaussian_prediction = []
  for data in positive_list:
    data = data / image_width
    if neutral_gaussian.pdf(data) > increment_gaussian.pdf(data):
      gaussian_prediction.append(0)
    else:
      gaussian_prediction.append(1)
  
  return gaussian_prediction

def print_lines(lines):
  for point in lines:
    print(f"{point}")


# Approach One
def find_cluster_mean(lines, line_num):
  print("Target line:")
  print(lines[line_num - 1])
  print("\n")
  print("Previous lines:")
  distance_dict = {}
  for i in range(line_num - 2, -1, -1):
    if lines[i]['indentation_factor'] not in distance_dict:
      distance_dict[lines[i]['indentation_factor']] = []
    distance_dict[lines[i]['indentation_factor']].append(abs(lines[i]['x'] - lines[line_num - 1]['x']))
  
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


# Approach Two
def find_cluster_nearest_neighbour(lines, line_num):
  # print("Target line:")
  # print(lines[line_num - 1])
  
  distance_dict = {}
  for i in range(line_num - 2, -1, -1):
    if lines[i]['indentation_factor'] not in distance_dict:
      distance_dict[lines[i]['indentation_factor']] = []
      distance_dict[lines[i]['indentation_factor']].append(abs(lines[i]['x'] - lines[line_num - 1]['x']))
  
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


def create_code_from_gaussian_indentation(lines):
  result = ''
  for data in lines:
      result += f"{INDENTATION * data['indentation_factor']}{data['text']}\n"
      
  return result
  

# Draw it all on goodnotes 109project notebook
def process_gaussian_indentation(lines, increment_label, neutral_label):
  modified_lines = copy.deepcopy(lines)
  
  for i in range(len(modified_lines)):
    modified_lines[i]['indentation_factor'] = 0
  
  for i in range(len(modified_lines)):
    if i != 0:
      
      if modified_lines[i]['delta_type'] == 'positive':
        
        if modified_lines[i]['gaussian_prediction'] == increment_label:
          modified_lines[i]['indentation_factor'] = modified_lines[i - 1]['indentation_factor'] + 1
          
        elif modified_lines[i]['gaussian_prediction'] == neutral_label:
          modified_lines[i]['indentation_factor'] = modified_lines[i - 1]['indentation_factor']
          
      elif modified_lines[i]['delta_type'] == 'negative':
        # cluster_mean = find_cluster_mean(modified_lines, i + 1)
        cluster_nn = find_cluster_nearest_neighbour(modified_lines, i + 1)
        # print(f"cluster_mean: {cluster_mean}")
        # print(f"cluster_nn: {cluster_nn}")
        modified_lines[i]['indentation_factor'] = cluster_nn
      
      elif modified_lines[i]['delta_type'] == 'null':
        modified_lines[i]['indentation_factor'] = modified_lines[i - 1]['indentation_factor']
    else:
      modified_lines[i]['indentation_factor'] = 0
  
  
  return modified_lines




def main(args):
  IMAGE_ID = int(args.image_id)

  with open('output/postprocessed_ocr_provider_data.json') as f:
      data = json.load(f)

  metadata = data[IMAGE_ID]

  # # get all x's into a list
  # x_coordinates = [point['x'] for point in lines]
  # deltas = [x_coordinates[n] - x_coordinates[n - 1] for n in range(1, len(x_coordinates))]

  # modified_lines = annotate_deltas(lines, deltas)
  # #print(f"modified_lines, after annotated deltas:\n {modified_lines}")
  
  # gaussian_prediction = get_gaussian_prediction(modified_lines, IMAGE_ID)
  # print(f"gaussian_prediction:\n {gaussian_prediction}")
  
  # modified_lines = add_gaussian_prediction_labels(modified_lines, gaussian_prediction) # For delta type positive adds gaussian Label, for {negative, null, and and none} adds None to gaussian Prediction Lable
  # increment_label, neutral_label = '1', '0'
  # # print_lines(modified_lines)
  
  
  # modified_lines = process_gaussian_indentation(modified_lines, increment_label, neutral_label)
  
  # print("\n\n")
  # code = create_code_from_gaussian_indentation(modified_lines)
  # print(f"{code}")
  image_path = f'../images/{IMAGE_ID}.jpg'
  image_width = cv2.imread(image_path).shape[1]
  
  result = GaussianIndentationRecognitionAlgo('nearest_neighbour').recognize_indents(metadata, image_width)

  lm_post_processed_code = SIMPLEprompting_test3.post_correction(result)
  

  print(result['ir_algo_output_code'])
  print(lm_post_processed_code)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-id", required=True, help="Give the image ID")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
    
    