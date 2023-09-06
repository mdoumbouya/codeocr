import pandas as pd
import json
from global_utils import *

with open('../apipayload.json', 'r') as json_file:
    data = json.load(json_file)
    
    
with open('../groundtruth.csv', 'r') as csv_file:
    gt = pd.read_csv(csv_file)

var = data[4]['Azure']

api_data = var["readResult"]['pages'][0]['lines']

line_info = line_data(api_data)
    
    
line_info = indent(line_info)

print(gt['Ground Truth'][4])
print(line_info)