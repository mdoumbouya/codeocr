import pandas as pd
import json
import csv
from code_ocr.global_utils import *
import editdistance
import time
from tqdm import tqdm
import argparse
from code_ocr.lm_post_correction import COTprompting

COTprompting = COTprompting()

def main(args):
    
    start_time = time.time() 
    with open(args.input_file, 'r') as json_file:
        data = json.load(json_file)
        
    with open('../rawdata.csv', 'r') as csv_file:
        rd = pd.read_csv(csv_file)

    extended_records = []
    
    for document_metadata in tqdm(data, desc='record'):
        
        # if "ir_algo_param_bandwidth" in document_metadata:
        #     if document_metadata["ir_algo_param_bandwidth"] == "estimated":
        image_id = document_metadata['image_id']
        ground_truth = rd['Ground Truth'][image_id]
        
        if args.prompting_method == "cot":
          document_metadata["lm_post_processed_code"] = COTprompting.post_correction(document_metadata)
        else:
          raise NotImplementedError(f"Prompting method {args.prompting_method} not implemented")
        
        document_metadata["lm_post_processed_edit_distance"] = editdistance.eval(document_metadata["lm_post_processed_code"], ground_truth)
        
        extended_records.append(document_metadata)
        
        time.sleep(1)



    with open(args.output_file, 'w') as output_file:
        json.dump(extended_records, output_file)
        


    end_time = time.time()  # save end time
    elapsed_time = end_time - start_time  # calculate elapsed time

    print(f"The code took {elapsed_time} seconds to run.")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", required=True, help="input file recognized indentation file")
    parser.add_argument("--output-file", required=True, help="file in which to put the new lm code")
    parser.add_argument("--prompting-method", required=True, help="Specify the method of prompting, or choose all")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
