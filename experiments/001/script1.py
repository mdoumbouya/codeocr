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
    

bandwidths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

def prepare_csv():
    with open('exp001result.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # write the header
        writer.writerow(['Ground Truth', 'Model Temperature', 
                            '0', '0 ED', '1', '1 ED', '2', '2 ED', '3', '3 ED', '4', '4 ED', '5', '5 ED', 
                            '6', '6 ED', '7', '7 ED', '8', '8 ED', '9', '9 ED', '10', '10 ED', '11', '11 ED', 
                            '12', '12 ED', '13', '13 ED', '14', '14 ED', '15', '15 ED', '16', '16 ED', 
                            '17', '17 ED', '18', '18 ED', '19', '19 ED', '20', '20 ED', '21', '21 ED', 
                            '22', '22 ED', '23', '23 ED', '24', '24 ED', '25', '25 ED', '26', '26 ED', 
                            '27', '27 ED', '28', '28 ED', '29', '29 ED', '30', '30 ED', '31', '31 ED', 
                            '32', '32 ED', '33', '33 ED', '34', '34 ED', '35', '35 ED', '36', '36 ED', 
                            '37', '37 ED', '38', '38 ED', '39', '39 ED', '40', '40 ED', '41', '41 ED', 
                            '42', '42 ED', '43', '43 ED', '44', '44 ED', '45', '45 ED', '46', '46 ED', 
                            '47', '47 ED', '48', '48 ED', '49', '49 ED', '50', '50 ED'])

prepare_csv()


with open('../groundtruth.csv', 'r') as csv_file:
    gt = pd.read_csv(csv_file)



for i in tqdm(range(55), desc='Image'):
    
    # print("This is Image ID: ", i)
    row = []
    ground_truth = gt['Ground Truth'][i]
    
    row.append(ground_truth)

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