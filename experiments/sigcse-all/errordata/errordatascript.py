import pandas as pd
import csv

from code_ocr.global_utils import *

data = pd.read_csv('errordata/derrorresults.csv')

def prepare_csv():
    with open('linebyline.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # write the header
        writer.writerow(['Data Id',
                            'Model Temperature',
                            'Ground Truth',
                            'Azure', 
                            'Line by Line LM', 
                            'Change Category Low',
                            ])
    
prepare_csv()

loop_size = len(data['Ground Truth'])

for i in range(10):
  row = []
  
  row.append(i)
  row.append(0.2)
  row.append(data['Ground Truth'][i])
  
  azureresult = data['Azure'][i]
  row.append(azureresult)
  final_result = lm_eachline(azureresult)
  row.append(final_result)
  
  
  # row.append(data['Azure LM Low'][i])
  row.append('null')
  # row.append(data['Azure LM Medium'][i])
  # row.append('null')
  # row.append(data['Azure LM High'][i])
  # row.append('null')
  
  with open('errordata/linebyline.csv', 'a', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(row)
  