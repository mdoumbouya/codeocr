import pandas as pd
import json
import csv
from global_utils import *
import editdistance
import time
from tqdm import tqdm
import argparse


def main(args):

    start_time = time.time() 
    with open(args.input_file, 'r') as json_file:
        data = json.load(json_file)
        

    bandwidths = range(args.bandwidth_min, args.bandwidth_max, args.bandwidth_step)
    print("bandwidths", list(bandwidths))
    


    with open('../rawdata.csv', 'r') as csv_file:
        rd = pd.read_csv(csv_file)


    extended_records = []
    for ocr_metadata in tqdm(data, desc='record'):
        image_id = ocr_metadata['image_id']
        ocr_metadata['ocr_provider']
        ocr_metadata['ocr_ouptut']
        ground_truth = rd['Ground Truth'][image_id]
        
        for bandwidth in tqdm(bandwidths, desc='bandwidth', leave=False):
            lines = ocr_metadata["ocr_ouptut"]
            final_code = indent(lines, bandwidth)
            ocr_metadata["rec_v1_bandwidth"] = bandwidth
            ocr_metadata["rec_v1_output"] = final_code
            ocr_metadata["rec_v1_output_edit_distance"] = editdistance.eval(ground_truth, final_code)
            extended_records.append(
                ocr_metadata
            )
            print(ocr_metadata)
        
        with open(args.output_file, 'w') as output_file:
            json.dump(extended_records, output_file)
        


    end_time = time.time()  # save end time
    elapsed_time = end_time - start_time  # calculate elapsed time

    print(f"The code took {elapsed_time} seconds to run.")


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
