import argparse
from pathlib import Path
import json
import shutil
import time
import pandas as pd
from tqdm import tqdm
import numpy as np
from scipy.stats import sem
import latextable
import texttable

"""
1. Read in the json file
2. Read in the rawdata.csv file
3. For each record in the json file, get the image id
4. Get the ground truth from the rawdata.csv file
5. Calculate the lenght of ground truth
6. Calculate the edit distance between the ground truth and the lm post processed code
7. Calculate the edit distance between the ground truth and the ir algo output code
8. Convert all the edit distance in percentages
9. Measure the mean of perecentage in each case.
10. Show the results.
"""



def main(args):

    start_time = time.time()
    
    with open(args.input_file, 'r') as json_file:
        data = json.load(json_file)
        
    with open('../rawdata.csv', 'r') as csv_file:
        rd = pd.read_csv(csv_file)
        
        
    ir_algo_output_edit_distance_percentage = []
    lm_post_processed_edit_distance_percentage = []

    for document_metadata in tqdm(data, desc='record'):
        
        image_num = document_metadata['image_id']
        
        ground_truth = rd['Ground Truth'][image_num]
        
        ground_truth_length = len(ground_truth)
        
        ir_algo_percentage = round((document_metadata["ir_algo_output_edit_distance"] / ground_truth_length * 100), 2)
        lm_post_processed_percentage = round((document_metadata["lm_post_processed_edit_distance"] / ground_truth_length * 100), 2)
        
        ir_algo_output_edit_distance_percentage.append(ir_algo_percentage)
        lm_post_processed_edit_distance_percentage.append(lm_post_processed_percentage)

    mean_ir_algo_output_edit_distance_percentage = round(np.mean(ir_algo_output_edit_distance_percentage), 2)
    mean_lm_post_processed_edit_distance_percentage = round(np.mean(lm_post_processed_edit_distance_percentage), 2)

    
    print("THE RESULT")
    
    result1 = f"Mean edit distance percentage for IR algo output: {mean_ir_algo_output_edit_distance_percentage}"
    result2 = f"Mean edit distance percentage for LM post processed code: {mean_lm_post_processed_edit_distance_percentage}"
    
    with open(args.output_file, 'w') as output_file:
        output_file.write(result1 + "\n")
        output_file.write(result2 + "\n")
        
    print(result1)
    print(result2)
    
    
    end_time = time.time()  # save end time
    elapsed_time = end_time - start_time  # calculate elapsed time
    print(f"The code took {elapsed_time} seconds to run.")
    
    



def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", required=True, help="input file. in common pipeline json format")
    parser.add_argument("--output-file", required=True, help="output file for results")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
