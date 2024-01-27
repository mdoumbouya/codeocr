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


# If I ever come back to this, one potential place of development is implement gpt4-vision more coherently with the codebase. 

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
GPT4_Vision = GPT4_Vision()

# A list of tuples, each tuple contains the prompting method and the post correction method
lm_post_correction_methods = [
    ("none", no_lmpc.post_correction),
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
    for document_metadata in tqdm(data, desc='Iteration through Indentation Recognition Algorithms for Post Correction'):
        if (document_metadata['ir_algo_name'] == 'none'
        or (document_metadata['ir_algo_name'] == 'meanshift-v1' and document_metadata['ir_algo_param_bandwidth'] == 'estimated')
        or (document_metadata['ir_algo_name'] == 'gaussian-v1')):
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

    # This part works with GPT4 vision
    if 'gpt4-vision' in args.post_correction_methods:
        image_dir = '../images/'
        for image_file in tqdm(os.listdir(image_dir), desc='Iteration through GPT4 Vision'):
            image_id = int(image_file.split('.')[0])
            if image_id not in rd.index:
                continue
            ground_truth = rd.loc[image_id, 'Ground Truth']
            image_path = image_dir + image_file
            image = cv2.imread(image_path)
            image_height, image_width, _ = image.shape
            gpt4v_output = GPT4_Vision.post_correction(image_path)
            gpt4v_output_edit_distance = editdistance.eval(gpt4v_output, ground_truth)
            
            document_metadata = {
                "image_id": image_id,
                "image_height": image_height,
                "image_width": image_width,
                "ocr_provider": "GPT4-vision",
                "ocr_ouptut": gpt4v_output,
                "ir_algo_name": "none",
                "ir_algo_output_code": gpt4v_output,
                "ir_algo_output_edit_distance": gpt4v_output_edit_distance,
                "prompting_method": "none",
                "lm_post_processed_code": gpt4v_output,
                "lm_post_processed_edit_distance": gpt4v_output_edit_distance,
            }
            
            extended_records.append(document_metadata)
            
        
        
    with open(args.output_file, 'w') as output_file:
        json.dump(extended_records, output_file)
        
    end_time = time.time()  # save end time
    elapsed_time = end_time - start_time  # calculate elapsed time
    
    logger.info(f"The lm_post_correction.py took {round((elapsed_time / 60), 2)} minutes to run.")

def parse_arguments():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", required=True, help="input file recognized indentation file")
    parser.add_argument("--output-file", required=True, help="file in which to put the new lm code")
    parser.add_argument("--post-correction-methods", required=True, nargs='+', help="Specify the methods of prompting, or choose all", choices=["none", "cot", "cot-test1", "cot-test2", "cot-test3", "cot-test4", "cot-test5", "simple", "simple-test1", "simple-test2", "simple-test3", "gpt4-vision"])
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
