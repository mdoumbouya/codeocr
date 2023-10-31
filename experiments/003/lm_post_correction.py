import pandas as pd
import json
import csv
from code_ocr.global_utils import *
import editdistance
import time
from tqdm import tqdm
import argparse
from code_ocr.post_correction import *
import copy
import logging


# If I ever come back to this, one potential place of development is implement gpt4b more coherently with the codebase. 

logger = logging.getLogger(__name__)

no_lmpc = no_lmpc()
COTprompting = COTprompting()
COTprompting_test1 = COTprompting_test1()
COTprompting_test2 = COTprompting_test2()
COTprompting_test3 = COTprompting_test3()
COTprompting_test4 = COTprompting_test4()
COTprompting_test5 = COTprompting_test5()
SIMPLEprompting = SIMPLEprompting()
SIMPLEprompting_test1 = SIMPLEprompting_test1()
SIMPLEprompting_test2 = SIMPLEprompting_test2()
SIMPLEprompting_test3 = SIMPLEprompting_test3()
#GPT$B is not added as a method here as I recieve it from a different dataset.

# A list of tuples, each tuple contains the prompting method and the post correction method
lm_post_correction_methods = [
    ("none", no_lmpc),
    ("cot", COTprompting.post_correction),
    ("cot-test1", COTprompting_test1.post_correction),
    ("cot-test2", COTprompting_test2.post_correction),
    ("cot-test3", COTprompting_test3.post_correction),
    ("cot-test4", COTprompting_test4.post_correction),
    ("cot-test5", COTprompting_test5.post_correction),
    ("simple", SIMPLEprompting.post_correction),
    ("simple-test1", SIMPLEprompting_test1.post_correction),
    ("simple-test2", SIMPLEprompting_test2.post_correction),
    ("simple-test3", SIMPLEprompting_test3.post_correction),
]

def main(args):
    start_time = time.time() 

    with open(args.input_file, 'r') as json_file:
        data = json.load(json_file)
        
    rd = pd.read_csv('../rawdata.csv')

    selected_lm_post_correction_methods = [
        m for m in lm_post_correction_methods if m[0] in args.post_correction_methods
    ]

    extended_records = []
    for document_metadata in tqdm(data, desc='Iteration'):
        if document_metadata['ir_algo_name'] == 'none' or (document_metadata['ir_algo_name'] == 'meanshift-v1' and document_metadata['ir_algo_param_bandwidth'] == 'estimated'):
            image_id = document_metadata['image_id']
            ground_truth = rd.loc[image_id, 'Ground Truth']

            for prompting_method, post_correction_algo in selected_lm_post_correction_methods:
                lm_post_processed_code = post_correction_algo(document_metadata)
                
                # This part is to log where it failed, if it failed.
                if lm_post_processed_code == 'failed':
                    logger.info(f"Failed to post process image {image_id}-> prompting method {prompting_method} -> ir algo{document_metadata['ir_algo_name']}")
                
                # The code would still continue to run, but the lm_post_processed_code would be 'failed'
                lm_post_processed_edit_distance = editdistance.eval(lm_post_processed_code, ground_truth)
                
                extended_record = {
                    **document_metadata, 
                    "prompting_method": prompting_method,
                    "lm_post_processed_code": lm_post_processed_code,
                    "lm_post_processed_edit_distance": lm_post_processed_edit_distance
                }
                extended_records.append(extended_record)

            
    if 'gpt4b' in args.post_correction_methods:
        with open('output/gpt4b_multimodal_manual.json') as f:
            gpt4b_data = json.load(f)
            
        for datum in gpt4b_data:
            extended_records.append(datum)

    with open(args.output_file, 'w') as output_file:
        json.dump(extended_records, output_file)
        
    end_time = time.time()  # save end time
    elapsed_time = end_time - start_time  # calculate elapsed time
    
    logger.info(f"The lm_post_correction.py took {round((elapsed_time / 60), 2)} minutes to run.")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", required=True, help="input file recognized indentation file")
    parser.add_argument("--output-file", required=True, help="file in which to put the new lm code")
    parser.add_argument("--post-correction-methods", required=True, nargs='+', help="Specify the methods of prompting, or choose all", choices=["none", "cot", "cot-test1", "cot-test2", "cot-test3", "cot-test4", "cot-test5", "simple", "simple-test1", "simple-test2", "simple-test3", "gpt4b"])
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
