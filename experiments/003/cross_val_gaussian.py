import json
import cv2
from pprint import pprint
import argparse
import copy
from code_ocr.indentation_recognition import GaussianIndentationRecognitionAlgo
from tqdm.auto import tqdm
import random

# Data points
DATA_POINTS = [1, 4, 7, 9, 11, 17, 21, 24, 26, 27, 28, 32, 39, 47, 48, 51]

RANDOM_SEED = 23


with open('./output/postprocessed_ocr_provider_data.json') as f:
    RAW_DATA = json.load(f)


# Leave-One-Out Cross-Validation (LOOCV)
def loocv(data):
    loocv_data = []
    for i in range(len(data)):
        # Extract the test item
        test = data[i]
        # Extract all items except the one at index i for training
        train = data[:i] + data[i+1:]
        # Append both train and test sets to the loocv_data list
        loocv_data.append({'train': train, 'test': test})
    
    return loocv_data


# print("Leave-One-Out Cross-Validation")
# loccv_data = loocv(DATA_POINTS)
# pprint(loccv_data)

# 5-Fold Cross-Validation
def k_fold(data, k=5):
    k_fold_data = []
    fold_sizes = [len(data) // k + (1 if i < len(data) % k else 0) for i in range(k)]
    folds = []
    current = 0

    # Create the folds
    for size in fold_sizes:
        folds.append(data[current:current + size])
        current += size

    # Create train and test datasets for each fold
    for i in range(k):
        test = folds[i]
        train = []
        # Collect all data except the one at folds[i] for training
        for j in range(k):
            if j != i:
                train += folds[j]
        k_fold_data.append({'train': train, 'test': test})

    return k_fold_data



# print("5-Fold Cross-Validation")
# k_fold_data = k_fold(DATA_POINTS, k=5)
# pprint(k_fold_data)

def eval_single_image(model, test_image_id, label_data):
  
    accruacy = {'test_image_id': test_image_id, 'predicted': 0, 'correct': 0}
    
    predicted = model.recognize_indents(RAW_DATA[test_image_id])
    
    for i in range(len(predicted['ir_algo_output_indented_lines'])):

        if predicted['ir_algo_output_indented_lines'][i]['gaussian_prediction'] == label_data[test_image_id]['ocr_ouptut'][i]['positive_indentation']:
            accruacy['correct'] += 1
        accruacy['predicted'] += 1
    
    # print(f"Predicted:")
    # pprint(predicted['ir_algo_output_indented_lines'])
    # print(f"Actual:")
    # pprint(label_data[test_image_id]['ocr_ouptut'])
    
    return accruacy
  
  
def filter_data(data, train_ids):
    return [item for item in data if item['image_id'] in train_ids]
  
def evaluate_loocv(data):
  
    data = copy.deepcopy(data)
    
    random.seed(RANDOM_SEED)
    random.shuffle(DATA_POINTS)
    
    loccv_data = loocv(DATA_POINTS)
    
    gaussian_model = GaussianIndentationRecognitionAlgo(negative_delta_cluster_method="nearest_ancestor")
    
    accuracies = []
    for i, datum in tqdm(enumerate(loccv_data)):
        train_ids = datum['train']
        
        train_metadata = filter_data(data, train_ids)
        train_image_widths = {str(item['image_id']): cv2.imread(f"../images/{item['image_id']}.jpg").shape[1] for item in train_metadata}
        gaussian_model.fit(train_image_widths, train_metadata)
        
        result_dict = {}
        result_dict['fold'] = i + 1
        result_dict['train'] = train_ids
        result_dict['neutral_mean'] = gaussian_model.neutral_mean
        result_dict['neutral_std'] = gaussian_model.neutral_std
        result_dict['increment_mean'] = gaussian_model.increment_mean
        result_dict['increment_std'] = gaussian_model.increment_std
        result_dict['test'] = datum['test']
        result_dict['accuracies'] = []
        result_dict['accuracies'].append(eval_single_image(gaussian_model, datum['test'], data))
        
        accuracies.append(result_dict)
    
    return accuracies


def eval_multiple_images(model, test_image_ids, label_data):
    accuracies = []
    for test_image_id in test_image_ids:
        accuracies.append(eval_single_image(model, test_image_id, label_data))
        
    return accuracies


def evaluate_five_fold(data):
    data = copy.deepcopy(data)
    
    random.seed(RANDOM_SEED)
    random.shuffle(DATA_POINTS)
    
    k_fold_data = k_fold(DATA_POINTS, k=5)
    
    gaussian_model = GaussianIndentationRecognitionAlgo(negative_delta_cluster_method="nearest_ancestor")
    
    accuracies = []
    for i, datum in tqdm(enumerate(k_fold_data)):
        train_ids = datum['train']
        
        train_metadata = filter_data(data, train_ids)
        train_image_widths = {str(item['image_id']): cv2.imread(f"../images/{item['image_id']}.jpg").shape[1] for item in train_metadata}
        gaussian_model.fit(train_image_widths, train_metadata)
        
        result_dict = {}
        result_dict['fold'] = i + 1
        result_dict['train'] = train_ids
        result_dict['neutral_mean'] = gaussian_model.neutral_mean
        result_dict['neutral_std'] = gaussian_model.neutral_std
        result_dict['increment_mean'] = gaussian_model.increment_mean
        result_dict['increment_std'] = gaussian_model.increment_std
        result_dict['test'] = datum['test']
        
        result_dict['accuracies'] = eval_multiple_images(gaussian_model, datum['test'], data)
        
        accuracies.append(result_dict)
  
    return accuracies
  

def construct_result_dict(method, result):
    return {
        'method': method,
        'result': result
    }

def main(args):
    with open('./labels-gaussian-process/labeled_data.json') as f:
        data = json.load(f)
    
    result = []
    
    if 'LOOCV' in args.cross_val_folds:
        result.append(construct_result_dict('LOOCV', evaluate_loocv(data)))
    
    if '5-Fold' in args.cross_val_folds:
        result.append(construct_result_dict('5-Fold', evaluate_five_fold(data)))
    
    with open('./output/cross_val_result.json', 'w') as f:
        json.dump(result, f)
    


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cross-val-folds", required=True, nargs='+', help="Specify the methods/folds for cross validation", choices=["LOOCV", "5-Fold"])
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
