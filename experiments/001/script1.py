import pandas as pd
import json
import csv
from global_utils import *
import editdistance
import time
from tqdm import tqdm


start_time = time.time() 


with open('../apipayload.json', 'r') as json_file:
    data = json.load(json_file)
    

bandwidths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]

def prepare_csv():
    with open('exp001result.csv', 'a', newline='') as csv_file:
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
        
    with open('exp001result.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)
    


end_time = time.time()  # save end time
elapsed_time = end_time - start_time  # calculate elapsed time

print(f"The code took {elapsed_time} seconds to run.")