"""
This file takes in the results from output from output/lm_post_processed.json and filters out some specific results, 
and then stores the filtered results in a new file called output/lm_post_processed_filtered.json
"""
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



def main(args):
    with open(args.input_file, 'r') as json_file:
        data = json.load(json_file)
        
    for document_metadata in tqdm(data):
        filtered_data = []
        modifiable_document_metadata = copy.deepcopy(document_metadata)

        if document_metadata['image_id'] not in args.filter_out:
            filtered_data.append(modifiable_document_metadata)
        
    with open(args.output_file, 'w') as json_file:
        json.dump(filtered_data, json_file)
            



def parse_arguments():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", required=True, help="input file recognized indentation file")
    parser.add_argument("--output-file", required=True, help="file in which to put the new lm code")
    parser.add_argument("--filter-out", required=True, help="Image ID's to filter out")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
