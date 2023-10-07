import pandas as pd
import json
import csv
from code_ocr.global_utils import *
import editdistance
import time
from tqdm import tqdm
import argparse
from code_ocr.indentation_recognition import IgnoreIndentRecognitionAlgo, MeanShiftIndentRecognitionAlgo



def build_indent_recognition_methods(args):
    indent_rec_methods = [
        IgnoreIndentRecognitionAlgo(),
        MeanShiftIndentRecognitionAlgo(bandwidth="estimated")
    ]
    
    indent_rec_methods.extend([
        MeanShiftIndentRecognitionAlgo(bandwidth=b) 
        for b in range(args.bandwidth_min, args.bandwidth_max, args.bandwidth_step)
    ])
    return indent_rec_methods


def main(args):
    
    start_time = time.time() 
    with open(args.input_file, 'r') as json_file:
        data = json.load(json_file)
        
    indent_recognition_methods = build_indent_recognition_methods(args)

    with open('../rawdata.csv', 'r') as csv_file:
        rd = pd.read_csv(csv_file)

    extended_records = []
    for document_metadata in tqdm(data, desc='record'):
        image_id = document_metadata['image_id']
        # document_metadata['ocr_provider']
        # document_metadata['ocr_ouptut']
        ground_truth = rd['Ground Truth'][image_id]
        
        for indent_recognition_method in indent_recognition_methods:
            document_medatada = indent_recognition_method.recognize_indents(document_metadata)
            document_medatada["ir_algo_output_edit_distance"] = editdistance.eval(ground_truth, document_medatada["ir_algo_output_code"]) 
            extended_records.append(document_medatada)

    with open(args.output_file, 'w') as output_file:
        json.dump(extended_records, output_file)
        


    end_time = time.time()  # save end time
    elapsed_time = end_time - start_time  # calculate elapsed time




def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", required=True, help="input file. api dump file")
    parser.add_argument("--output-file", required=True, help="file in which to generate code")
    parser.add_argument("--bandwidth-min", default=1, type=int)
    parser.add_argument("--bandwidth-max", default=200, type=int)
    parser.add_argument("--bandwidth-step", default=5, type=int)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
