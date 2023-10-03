import argparse
from pathlib import Path
import json
import shutil
import time
import pandas as pd
from tqdm import tqdm
import numpy as np
from scipy.stats import sem, tstd
from scipy import mean
import latextable
import texttable
from code_ocr.lm_post_correction import COTprompting, SIMPLEprompting
import copy
import editdistance


COTprompting = COTprompting()
SIMPLEprompting = SIMPLEprompting()

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

    missing_data = []
    
    fixed_data = []
    
    for document_metadata in tqdm(data, desc='record'):
        
        if document_metadata['lm_post_processed_code'] != '':
            fixed_data.append(document_metadata)
            
            image_num = document_metadata['image_id']
            
            ground_truth = rd['Ground Truth'][image_num]
            
            ground_truth_length = len(ground_truth)
            
            ir_algo_percentage = round((document_metadata["ir_algo_output_edit_distance"] / ground_truth_length * 100), 2)
            lm_post_processed_percentage = round((document_metadata["lm_post_processed_edit_distance"] / ground_truth_length * 100), 2)
            
            ir_algo_output_edit_distance_percentage.append(ir_algo_percentage)
            lm_post_processed_edit_distance_percentage.append(lm_post_processed_percentage)
            
            
    mean_ir_algo_output_edit_distance_percentage = round(mean(ir_algo_output_edit_distance_percentage), 2)
    mean_lm_post_processed_edit_distance_percentage = round(mean(lm_post_processed_edit_distance_percentage), 2)
    
    tstd_ir_algo_output_edit_distance_percentage = round(tstd(ir_algo_output_edit_distance_percentage), 2)
    tstd_lm_post_processed_edit_distance_percentage = round(tstd(lm_post_processed_edit_distance_percentage), 2)
    
    sem_ir_algo_output_edit_distance_percentage = round(sem(ir_algo_output_edit_distance_percentage), 2)
    sem_lm_post_processed_edit_distance_percentage = round(sem(lm_post_processed_edit_distance_percentage), 2)

    
    print("THE RESULT")
    
    result1mean = f"Mean edit distance percentage for IR algo output: {mean_ir_algo_output_edit_distance_percentage}"
    result1tstd = f"tstd edit distance percentage for IR algo output: {tstd_ir_algo_output_edit_distance_percentage}"
    result1sem = f"sem edit distance percentage for IR algo output: {sem_ir_algo_output_edit_distance_percentage}"
    
    
    
    result2mean = f"Mean edit distance percentage for LM post processed code: {mean_lm_post_processed_edit_distance_percentage}"
    result2tstd = f"tstd edit distance percentage for LM post processed code: {tstd_lm_post_processed_edit_distance_percentage}"
    result2sem = f"sem edit distance percentage for LM post processed code: {sem_lm_post_processed_edit_distance_percentage}"
    
    with open(args.output_file, 'w') as output_file:
        json.dump(fixed_data, output_file)
        
        
        
    print(result1mean)
    print(result1tstd)
    print(result1sem)
    
    
    
    print(result2mean)
    print(result2tstd)
    print(result2sem)
    
    
    print("MISSING DATA")
    for missing_tuple in missing_data:
        print(missing_tuple)
    print(f"Total missing data: {len(missing_data)}")
    
    
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
