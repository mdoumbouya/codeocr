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
    
    def prepare_csv():
        with open(args.output_file, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)

            # write the header
            header = ['Ground Truth', 'Azure', 'Azure ED']
            for i in range(1, 101):
                header.append(str(i))
                header.append(str(i) + ' ED')
            writer.writerow(header)

    prepare_csv()


    with open('../rawdata.csv', 'r') as csv_file:
        rd = pd.read_csv(csv_file)



    for i in tqdm(range(55), desc='Image'):
        
        # print("This is Image ID: ", i)
        row = []
        ground_truth = rd['Ground Truth'][i]
        
        row.append(ground_truth)
        
        row.append(rd['Azure'][i])
        row.append(editdistance.eval(ground_truth, rd['Azure'][i]))
        

        var = data[i]['Azure']
        
        for bandwidth in tqdm(bandwidths, desc='bandwidth', leave=False):
            api_data = var["readResult"]['pages'][0]['lines']
            
            lines = line_data(api_data)
            
            final_code = indent(lines, bandwidth)

            row.append(final_code)
            
            row.append(editdistance.eval(ground_truth, final_code))
            # print("Bandwidth: ", bandwidth)
            
        with open(args.output_file, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(row)
        


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
