import copy
from sklearn.cluster import MeanShift, estimate_bandwidth
import numpy as np
from code_ocr.global_utils import avg_list
from scipy.stats import norm
from tqdm.auto import tqdm

class IndentationRecognitionAlgorithm(object):
    def __init__(self, name):
        self.name = name

    def recognize_indents(self, document_metadata):
        raise NotImplementedError()
    
    def construct_output(self, orig_document_metadta, params, outputs):
        generated_metadata = copy.deepcopy(orig_document_metadta)
        generated_metadata["ir_algo_name"] = self.name
        generated_metadata.update({f"ir_algo_param_{k}": v for k, v in params.items()})
        generated_metadata.update({f"ir_algo_output_{k}": v for k, v in outputs.items()})
        return generated_metadata


    
# Sazzad Note(SN): Ask Moussa how does this class work. 
class MeanShiftIndentRecognitionAlgo(IndentationRecognitionAlgorithm):
    def __init__(self, bandwidth):
        super().__init__("meanshift-v1")
        self.bandwidth = bandwidth

    def recognize_indents(self, document_metadata):
        params={
            "bandwidth": self.bandwidth
        }
        updated_document_metadata = copy.deepcopy(document_metadata)
        lines = updated_document_metadata["ocr_ouptut"]

        estimated_or_requested_bandwidth = self.bandwidth
        if self.bandwidth == "estimated":
            params["estimated_bandwidth"] = self.estimate_bandwidth(document_metadata)
            estimated_or_requested_bandwidth = params["estimated_bandwidth"]
        
        lines, final_code = meanshift_indentation_recognition(lines, estimated_or_requested_bandwidth)

        return self.construct_output(
            document_metadata, 
            params=params,
            outputs={
                "code": final_code,
                "indented_lines": lines
            }
        )
    
    def estimate_bandwidth(self, document_metadata):
        # print(document_metadata.keys())
        box_heights = np.array([box["h"] for box in document_metadata['ocr_ouptut']])
        return np.mean(box_heights)*1.5
            
            
class GaussianIndentationRecognitionAlgo(IndentationRecognitionAlgorithm):
    def __init__(self, 
                negative_delta_cluster_method="nearest_ancestor", 
                neutral_mean=0.0072602999579008815 , 
                neutral_std=0.008279078889046027,
                increment_mean=0.0777810811891604, 
                increment_std=0.024844347044055918): # These values are the default values, collected from the experiments
        
        super().__init__("gaussian-v1")
        self.negative_delta_cluster_method = negative_delta_cluster_method
        self.neutral_mean = neutral_mean
        self.neutral_std = neutral_std
        self.increment_mean = increment_mean
        self.increment_std = increment_std
    
    def fit(self, image_widths, document_metadatas):
        """fit this takes input forom the labeled_data.json, and fits the model to the data

        :param image_widths: Width of the corresponding image
        :type image_widths: dictionary
        :param document_metadatas: metadat of the image
        :type document_metadatas: json list
        """
        neutral_list = []
        increment_list = []
        
        for document_metadata in document_metadatas:
            lines = document_metadata["ocr_ouptut"]
            
            for i in range(len(lines)):
                
                if i != 0:
                    
                    if lines[i]['positive_indentation'] == '0':
                        delta = lines[i]['x'] - lines[i - 1]['x']
                        normalized_delta = delta / image_widths[str(document_metadata['image_id'])]
                        
                        neutral_list.append(normalized_delta) 
                        
                    elif lines[i]['positive_indentation'] == '1':
                        delta = lines[i]['x'] - lines[i - 1]['x']
                        normalized_delta = delta / image_widths[str(document_metadata['image_id'])]
                        
                        increment_list.append(normalized_delta)
        
        self.neutral_mean = np.mean(neutral_list)
        self.neutral_std = np.std(neutral_list)
        self.increment_mean = np.mean(increment_list)
        self.increment_std = np.std(increment_list)
    
    def recognize_indents(self, document_metadata):
        params={
            "negative_delta_cluster_method": self.negative_delta_cluster_method, # If someone does not pass in a specific value from the possible values, the code will deafualt to "nearest_ancestor"
            "neutral_mean": self.neutral_mean,
            "neutral_std": self.neutral_std,
            "increment_mean": self.increment_mean,
            "increment_std": self.increment_std
        }
        
        image_width = document_metadata["image_width"]
        updated_document_metadata = copy.deepcopy(document_metadata)
        lines = updated_document_metadata["ocr_ouptut"]
        
        # Get all, the x into a list, and find the deltas.
        x_coordinates = [point['x'] for point in lines]
        deltas = [x_coordinates[n] - x_coordinates[n - 1] for n in range(1, len(x_coordinates))]
        
        # Annotate the data points with their corresponding delta values and delta types.
        lines = annotate_deltas(lines, deltas)

        # Get the Gaussian predictions for the 'delta' values of the data points where 'delta_type' is 'positive'.
        gaussian_prediction = get_gaussian_prediction(lines, image_width, self.neutral_mean, self.neutral_std, self.increment_mean, self.increment_std)
        
        # Add Gaussian prediction labels to the data points.
        lines = add_gaussian_prediction_labels(lines, gaussian_prediction)
        increment_label, neutral_label = '1', '0'
        
        # Process the indentation from the labels, and select the negative delta cluster method.
        lines = process_gaussian_indentation(lines, increment_label, neutral_label, self.negative_delta_cluster_method)
        
        # Extract final code from the lines.
        final_code = create_code_from_gaussian_indentation(lines)
        
        return self.construct_output(
            document_metadata, 
            params=params,
            outputs={
                "code": final_code,
                "indented_lines": lines
            }
        )



class IgnoreIndentRecognitionAlgo(IndentationRecognitionAlgorithm):
    def __init__(self):
        super().__init__("none")

    def recognize_indents(self, document_metadata):
        updated_document_metadata = copy.deepcopy(document_metadata)
        lines = updated_document_metadata["ocr_ouptut"]
        final_code = "\n".join([line["text"].strip() for line in lines])

        return self.construct_output(
            document_metadata, 
            params={}, 
            outputs={"code": final_code}
        )

'''
Helper Functions
'''

INDENTATION = '    '


"""
Meanshift Algorithm
"""
def meanshift_indentation_recognition(lines, bandwidth):
    lines = copy.deepcopy(lines)
    indentation = INDENTATION # 4 spaces
    
    # Data Preparation, getting all the x values from the lines json array
    x_values = [line['x'] for line in lines]
    x_values = np.array(x_values).reshape(-1, 1)
    
    # Running it through the mean shift algorithm
    mean_shift = MeanShift(bandwidth=bandwidth)
    mean_shift.fit(x_values)
    labels = mean_shift.labels_ # List of the labels for each line
    
    # print(labels)
    
    for i in range(len(lines)):
        lines[i]['cluster_label'] = int(labels[i])
        
    # Create a dictionary where the `key` is the label, and the `value` is a list of all `x` 
    # coordinates with the same label. `{label:[list of all the values of same label]}`
    label_coords = {}
    
    for i in range(len(lines)):
        if lines[i]['cluster_label'] not in label_coords:
            label_coords[lines[i]['cluster_label']] = []
        label_coords[lines[i]['cluster_label']].append(lines[i]['x'])
    
    # print(label_coords)
    
    # Find a the `average x` of each label, and store them in a dictionary where the key is label, 
    # and the value is average of all elements with that label. Structure: `{label: average of all values of that label`
    
    label_avgs = {}
    
    for label in label_coords:
        label_avgs[label] = avg_list(label_coords[label])
        
    # print(label_avgs)
    
    
    # `sort` the dictionary based on the values, 
    # and now you have a dictionary in the ascending order of level of indentation. 
    label_avgs = dict(sorted(label_avgs.items(), key=lambda item: item[1]))
    
    # print(label_avgs)
    
    # Make a list of keys of the dictionary. Then iterate through them using `i`, now the index of each 
    # element is the level of indentation. Find for it's matching label in the `lines json array`,
    # once the label matches set `i` as the level of indentation by creating a new key called `indentation` 
    # in each line.
    
    """
    Possible space for optimization
    """
    label_avg_lst = list(label_avgs.keys())
    
    # print(label_avg_lst)
    
    for i in range(len(label_avg_lst)):
        for line in lines:
            if line['cluster_label'] == label_avg_lst[i]:
                line['indentation'] = i
    
    final_code = ''
    
    
    # Now just iterate through the lines, and multiply the value of `indentation`, and get the resulting text.
    
    for i in range(len(lines)):
        final_code += indentation * lines[i]['indentation'] + lines[i]['text'] + '\n'
    
    # print(final_code)
    
    return lines, final_code


"""

# Function for Gaussian Algorithm

"""

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



def get_gaussian_prediction(lines, image_width, neutral_mean, neutral_std, increment_mean, increment_std):
    """
    This function performs Gaussian  prediction on the 'delta' values of the 
    data points where 'delta_type' is 'positive'.

    Parameters:
    lines (list): A list of dictionaries where each dictionary represents a data point. 
                        Each data point must have 'delta' and 'delta_type' keys.

    Returns:
    numpy.ndarray: Returns an array of Gaussian predictions for the 'delta' values of the data points 
                    where 'delta_type' is 'positive'. The length of this array is equal to the 
                    number of 'positive' delta_type in lines.
    """
    positive_list = []
    for data in lines:
        if data['delta_type'] == 'positive':
            positive_list.append(data['delta'])
    
    neutral_gaussian = norm(loc=neutral_mean, scale=neutral_std)
    increment_gaussian = norm(loc=increment_mean, scale=increment_std)
    
    gaussian_prediction = []
    for data in positive_list:
        data = data / image_width
        if neutral_gaussian.pdf(data) > increment_gaussian.pdf(data):
            gaussian_prediction.append(0)
        else:
            gaussian_prediction.append(1)
    
    return gaussian_prediction


def add_gaussian_prediction_labels(lines, gaussian_prediction):
    """
    This function adds Gaussian prediction labels to the data points.
    
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


# Draw it all on goodnotes 109project notebook
# I am changing the name indentation_factor to cluster_label
def process_gaussian_indentation(lines, increment_label, neutral_label, negative_delta_cluster_method):
    modified_lines = copy.deepcopy(lines)
    
    for i in range(len(modified_lines)):
        modified_lines[i]['cluster_label'] = 0
    
    for i in range(len(modified_lines)):
        if i != 0:
        
            if modified_lines[i]['delta_type'] == 'positive':
            
                if modified_lines[i]['gaussian_prediction'] == increment_label:
                    modified_lines[i]['cluster_label'] = modified_lines[i - 1]['cluster_label'] + 1
                
                elif modified_lines[i]['gaussian_prediction'] == neutral_label:
                    modified_lines[i]['cluster_label'] = modified_lines[i - 1]['cluster_label']
            
            elif modified_lines[i]['delta_type'] == 'negative':
                
                if negative_delta_cluster_method == 'mean':
                    identified_cluster_from_mean = find_cluster_from_mean(modified_lines, i + 1)
                    modified_lines[i]['cluster_label'] = identified_cluster_from_mean
                    
                else: # negative_delta_cluster_method == 'nearest_ancestor'
                    identified_cluster_from_nn = find_cluster_from_nearest_ancestors(modified_lines, i + 1)
                    modified_lines[i]['cluster_label'] = identified_cluster_from_nn
        
            elif modified_lines[i]['delta_type'] == 'null':
                modified_lines[i]['cluster_label'] = modified_lines[i - 1]['cluster_label']
        else:
            modified_lines[i]['cluster_label'] = 0
    
    
    return modified_lines


# Approach One
def find_cluster_from_mean(lines, line_num):
    distance_dict = {}
    for i in range(line_num - 2, -1, -1):
        if lines[i]['cluster_label'] not in distance_dict:
            distance_dict[lines[i]['cluster_label']] = []
            distance_dict[lines[i]['cluster_label']].append(abs(lines[i]['x'] - lines[line_num - 1]['x']))
    
    # print(distance_dict)
    for key in distance_dict:
        distance_dict[key] = np.mean(distance_dict[key])

    # Now we will sort the dictionary on the basis of the values in ascending order
    sorted_distance_dict = {k: v for k, v in sorted(distance_dict.items(), key=lambda item: item[1])}
    
    return list(sorted_distance_dict.keys())[0]


# Approach Two
def find_cluster_from_nearest_ancestors(lines, line_num):
    
    distance_dict = {}
    for i in range(line_num - 2, -1, -1):
        if lines[i]['cluster_label'] not in distance_dict:
            distance_dict[lines[i]['cluster_label']] = []
            distance_dict[lines[i]['cluster_label']].append(abs(lines[i]['x'] - lines[line_num - 1]['x']))
    
    sorted_distance_dict = {k: v for k, v in sorted(distance_dict.items(), key=lambda item: item[1])}

    return list(sorted_distance_dict.keys())[0]


def create_code_from_gaussian_indentation(lines):
    result = ''
    for data in lines:
        result += f"{INDENTATION * data['cluster_label']}{data['text']}\n"
        
    return result