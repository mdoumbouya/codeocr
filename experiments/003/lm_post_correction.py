import pandas as pd
import json
import csv
from code_ocr.global_utils import *
import editdistance
import time
from tqdm import tqdm
import argparse
from code_ocr.lm_post_correction import COTprompting, SIMPLEprompting
import copy
import logging

logger = logging.getLogger(__name__)

COTprompting = COTprompting()
SIMPLEprompting = SIMPLEprompting()

# A list of tuples, each tuple contains the prompting method and the post correction method
lm_post_correction_methods = [
    ("cot", COTprompting.post_correction), 
    ("simple", SIMPLEprompting.post_correction)
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
        image_id = document_metadata['image_id']
        ground_truth = rd.loc[image_id, 'Ground Truth']

        for prompting_method, post_correction_algo in selected_lm_post_correction_methods:
            lm_post_processed_code = post_correction_algo(document_metadata)
            lm_post_processed_edit_distance = editdistance.eval(lm_post_processed_code, ground_truth)
            
            extended_record = {
                **document_metadata, 
                "prompting_method": prompting_method,
                "lm_post_processed_code": lm_post_processed_code,
                "lm_post_processed_edit_distance": lm_post_processed_edit_distance
            }
            extended_records.append(extended_record)

    with open(args.output_file, 'w') as output_file:
        json.dump(extended_records, output_file)
        
    end_time = time.time()  # save end time
    elapsed_time = end_time - start_time  # calculate elapsed time
    logger.info(f"The code took {elapsed_time} seconds to run.")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", required=True, help="input file recognized indentation file")
    parser.add_argument("--output-file", required=True, help="file in which to put the new lm code")
    parser.add_argument("--post-correction-methods", required=True, nargs='+', help="Specify the methods of prompting, or choose all", choices=["cot", "simple"])
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
