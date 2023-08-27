import pandas as pd
import csv
from global_utils import *
import editdistance


# Read in the data
df = pd.read_csv('FINAL DATA/bigdataset.csv')

loop_len = 55


def prepare_csv():
    with open('FINAL DATA/doubleprompted.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # write the header
        writer.writerow(['Ground Truth',
                            'GCV DP', # Google Computer Vision Starts Here
                            'ED GCV DP',
                            'AWS DP', # Amazon Web Services Starts Here
                            'ED AWS DP',
                            'Azure DP', # Azure Starts Here
                            'ED Azure DP',
                            'MP DP', # Mathpix Starts Here
                            'ED MP DP', 
                            ])
    
prepare_csv()



for i in range(loop_len):
    row = []
    row.append(remove_blank_lines(df['Ground Truth'][i]))
    
    #GCV
    GCV = df['GCV'][i]
    
    GCV_DP = double_prompt(GCV)
    row.append(GCV_DP)
    ED_GCV_DP = editdistance.eval(df['Ground Truth'][i], GCV_DP)
    row.append(ED_GCV_DP)
    time.sleep(1)
    
    #AWS
    AWS = df['AWS'][i]
    
    AWS_DP = double_prompt(AWS)
    row.append(AWS_DP)
    ED_AWS_DP = editdistance.eval(df['Ground Truth'][i], AWS_DP)
    row.append(ED_AWS_DP)
    time.sleep(1)
    
    #Azure
    Azure = df['Azure'][i]
    
    Azure_DP = double_prompt(Azure)
    row.append(Azure_DP)
    ED_Azure_DP = editdistance.eval(df['Ground Truth'][i], Azure_DP)
    row.append(ED_Azure_DP)
    time.sleep(1)
    
    #MP
    MP = df['MP'][i]
    
    MP_DP = double_prompt(MP)
    row.append(MP_DP)
    ED_MP_DP = editdistance.eval(df['Ground Truth'][i], MP_DP)
    row.append(ED_MP_DP)
    time.sleep(1)
    
    with open('FINAL DATA/doubleprompted.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)
    
    
    