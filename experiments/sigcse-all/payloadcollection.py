import pandas as pd
import csv
from code_ocr.global_utils import *
import editdistance


# Read in the data
df = pd.read_csv('FINAL DATA/bigdataset.csv')

loop_len = 55


def prepare_csv():
    with open('FINAL DATA/payload.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # write the header
        writer.writerow(['Ground Truth',
                            'Azure Raw',
                            'Simple Prompting Input', 
                            'Simple Prompting Output',
                            'CoT Prompting Input One', 
                            'CoT Prompting Output One',
                            'CoT Prompting Input Two', 
                            'CoT Prompting Output Two',
                            ])
    
prepare_csv()



for i in range(loop_len):
    row = []
    row.append(remove_blank_lines(df['Ground Truth'][i]))
    

    #Azure
    Azure = df['Azure'][i]
    
    row.append(Azure)
    
    simple_prompt_payload, simple_prompt_response_json = simple_prompt(Azure)
    
    row.append(simple_prompt_payload)
    row.append(simple_prompt_response_json)
    
    initial_payload, initial_response_json, final_payload, final_response_json = double_prompt_payload(Azure)
    
    row.append(initial_payload)
    row.append(initial_response_json)
    row.append(final_payload)
    row.append(final_response_json)
    

    time.sleep(1)
    

    with open('FINAL DATA/payload.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)
    
    print(i)
    
    
    