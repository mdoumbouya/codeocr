import pandas as pd
import csv
import requests
from PIL import Image
import editdistance
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from csv import writer
from pathlib import Path
from google.cloud import vision
from code_ocr.global_utils import *
import base64
from cleantext import clean
import black
from black import InvalidInput
import timeit



raw_data = pd.read_csv('FINAL DATA/bigdataset.csv')




# Preparing the CSV file

def prepare_csv(file_name):
    with open(file_name, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # write the header
        writer.writerow(['Ground Truth',
                            'Model Temperature', 
                            'GCV', # Google Computer Vision Starts Here
                            'ED GCV',
                            'GCV LM Low', 
                            'ED GCV LM Low', 
                            'GCV LM Medium', 
                            'ED GCV LM Medium', 
                            'GCV LM High', 
                            'ED GCV LM High',
                            'AWS', # Amazon Web Services Starts Here
                            'ED AWS',
                            'AWS LM Low', 
                            'ED AWS LM Low', 
                            'AWS LM Medium', 
                            'ED AWS LM Medium', 
                            'AWS LM High', 
                            'ED AWS LM High',
                            'Azure', # Azure Starts Here
                            'ED Azure',
                            'Azure LM Low', 
                            'ED Azure LM Low', 
                            'Azure LM Medium', 
                            'ED Azure LM Medium', 
                            'Azure LM High', 
                            'ED Azure LM High',  
                            'MP', # Mathpix Starts Here
                            'ED MP', 
                            'MP LM Low', 
                            'ED MP LM Low', 
                            'MP LM Medium', 
                            'ED MP LM Medium', 
                            'MP LM High', 
                            'ED MP LM High',
                            ])
    

prepare_csv('FINAL DATA/wcommentall.csv')
prepare_csv('FINAL DATA/woutcommentall.csv')
    
GROUND_TRUTH_LIST = []
for i in range(len(raw_data['Ground Truth'])):
    GROUND_TRUTH_LIST.append(fmt_code(str(raw_data['Ground Truth'][i])))


loop_count = len(raw_data['Ground Truth'])

for i in range(loop_count):
  wcomment_row = []
  woutcomment_row = []
  
  # Ground Truth
  ground_truth = fmt_code(remove_blank_lines(raw_data['Ground Truth'][i]))
  ground_truth_woutcomment = fmt_code(remove_blank_lines(remove_comments(ground_truth)))
  
  wcomment_row.append(ground_truth)
  woutcomment_row.append(ground_truth_woutcomment)
  
  # Model Temperature
  model_temperature = raw_data['Model Temperature'][i]
  
  wcomment_row.append(model_temperature)
  woutcomment_row.append(model_temperature)
  
  
  # GCV
  gcv = raw_data['GCV'][i]
  wcomment_row.append(gcv)
  woutcomment_row.append(remove_blank_lines(remove_comments(gcv)))
  
  ed_gcv = raw_data['ED GCV'][i]
  wcomment_row.append(ed_gcv)
  ed_gcv_woutcomment = editdistance.eval(ground_truth_woutcomment, remove_comments(gcv))
  woutcomment_row.append(ed_gcv_woutcomment)
  
  # GCV LM Low
  gcv_lm_low_wcomment = fmt_code(remove_blank_lines(raw_data['GCV LM Low'][i])) # With Comments
  wcomment_row.append(gcv_lm_low_wcomment)
  
  ed_gcv_lm_low_wcomment = editdistance.eval(ground_truth, gcv_lm_low_wcomment)
  wcomment_row.append(ed_gcv_lm_low_wcomment)
  
  
  gcv_lm_low_woutcomment = fmt_code(remove_blank_lines(remove_comments(gcv_lm_low_wcomment))) # Without Comments
  woutcomment_row.append(gcv_lm_low_woutcomment)
  
  ed_gcv_lm_low_woutcomment = editdistance.eval(ground_truth_woutcomment, gcv_lm_low_woutcomment)
  woutcomment_row.append(ed_gcv_lm_low_woutcomment)
  
  # GCV LM Medium
  gcv_lm_medium_wcomment = fmt_code(remove_blank_lines(raw_data['GCV LM Medium'][i])) # With Comments
  wcomment_row.append(gcv_lm_medium_wcomment)
  
  ed_gcv_lm_medium_wcomment = editdistance.eval(ground_truth, gcv_lm_medium_wcomment)
  wcomment_row.append(ed_gcv_lm_medium_wcomment)
  
  
  gcv_lm_medium_woutcomment = fmt_code(remove_blank_lines(remove_comments(gcv_lm_medium_wcomment))) # Without Comments
  woutcomment_row.append(gcv_lm_medium_woutcomment)
  
  ed_gcv_lm_medium_woutcomment = editdistance.eval(ground_truth_woutcomment, gcv_lm_medium_woutcomment)
  woutcomment_row.append(ed_gcv_lm_medium_woutcomment)
  
  # GCV LM High
  gcv_lm_high_wcomment = fmt_code(remove_blank_lines(raw_data['GCV LM High'][i])) # With Comments
  wcomment_row.append(gcv_lm_high_wcomment)
  
  ed_gcv_lm_high_wcomment = editdistance.eval(ground_truth, gcv_lm_high_wcomment)
  wcomment_row.append(ed_gcv_lm_high_wcomment)
  
  
  gcv_lm_high_woutcomment = fmt_code(remove_blank_lines(remove_comments(gcv_lm_high_wcomment))) # Without Comments
  woutcomment_row.append(gcv_lm_high_woutcomment)
  
  ed_gcv_lm_high_woutcomment = editdistance.eval(ground_truth_woutcomment, gcv_lm_high_woutcomment)
  woutcomment_row.append(ed_gcv_lm_high_woutcomment)
  
  
  # AWS
  AWS = raw_data['AWS'][i]
  wcomment_row.append(AWS)
  woutcomment_row.append(remove_blank_lines(remove_comments(AWS)))
  
  ed_AWS = raw_data['ED AWS'][i]
  wcomment_row.append(ed_AWS)
  ed_aws_woutcomment = editdistance.eval(ground_truth_woutcomment, remove_comments(AWS))
  woutcomment_row.append(ed_aws_woutcomment)
  
  # AWS LM Low
  AWS_lm_low_wcomment = fmt_code(remove_blank_lines(raw_data['AWS LM Low'][i])) # With Comments
  wcomment_row.append(AWS_lm_low_wcomment)
  
  ed_AWS_lm_low_wcomment = editdistance.eval(ground_truth, AWS_lm_low_wcomment)
  wcomment_row.append(ed_AWS_lm_low_wcomment)
  
  
  AWS_lm_low_woutcomment = fmt_code(remove_blank_lines(remove_comments(AWS_lm_low_wcomment))) # Without Comments
  woutcomment_row.append(AWS_lm_low_woutcomment)
  
  ed_AWS_lm_low_woutcomment = editdistance.eval(ground_truth_woutcomment, AWS_lm_low_woutcomment)
  woutcomment_row.append(ed_AWS_lm_low_woutcomment)
  
  # AWS LM Medium
  AWS_lm_medium_wcomment = fmt_code(remove_blank_lines(raw_data['AWS LM Medium'][i])) # With Comments
  wcomment_row.append(AWS_lm_medium_wcomment)
  
  ed_AWS_lm_medium_wcomment = editdistance.eval(ground_truth, AWS_lm_medium_wcomment)
  wcomment_row.append(ed_AWS_lm_medium_wcomment)
  
  
  AWS_lm_medium_woutcomment = fmt_code(remove_blank_lines(remove_comments(AWS_lm_medium_wcomment))) # Without Comments
  woutcomment_row.append(AWS_lm_medium_woutcomment)
  
  ed_AWS_lm_medium_woutcomment = editdistance.eval(ground_truth_woutcomment, AWS_lm_medium_woutcomment)
  woutcomment_row.append(ed_AWS_lm_medium_woutcomment)
  
  # AWS LM High
  AWS_lm_high_wcomment = fmt_code(remove_blank_lines(raw_data['AWS LM High'][i])) # With Comments
  wcomment_row.append(AWS_lm_high_wcomment)
  
  ed_AWS_lm_high_wcomment = editdistance.eval(ground_truth, AWS_lm_high_wcomment)
  wcomment_row.append(ed_AWS_lm_high_wcomment)
  
  
  AWS_lm_high_woutcomment = fmt_code(remove_blank_lines(remove_comments(AWS_lm_high_wcomment))) # Without Comments
  woutcomment_row.append(AWS_lm_high_woutcomment)
  
  ed_AWS_lm_high_woutcomment = editdistance.eval(ground_truth_woutcomment, AWS_lm_high_woutcomment)
  woutcomment_row.append(ed_AWS_lm_high_woutcomment)
  
  
  # Azure
  Azure = raw_data['Azure'][i]
  wcomment_row.append(Azure)
  woutcomment_row.append(remove_blank_lines(remove_comments(Azure)))
  
  ed_Azure = raw_data['ED Azure'][i]
  wcomment_row.append(ed_Azure)
  ed_azure_woutcomments = editdistance.eval(ground_truth_woutcomment, remove_comments(Azure))
  woutcomment_row.append(ed_azure_woutcomments)
  
  # Azure LM Low
  Azure_lm_low_wcomment = fmt_code(remove_blank_lines(raw_data['Azure LM Low'][i])) # With Comments
  wcomment_row.append(Azure_lm_low_wcomment)
  
  ed_Azure_lm_low_wcomment = editdistance.eval(ground_truth, Azure_lm_low_wcomment)
  wcomment_row.append(ed_Azure_lm_low_wcomment)
  
  
  Azure_lm_low_woutcomment = fmt_code(remove_blank_lines(remove_comments(Azure_lm_low_wcomment))) # Without Comments
  woutcomment_row.append(Azure_lm_low_woutcomment)
  
  ed_Azure_lm_low_woutcomment = editdistance.eval(ground_truth_woutcomment, Azure_lm_low_woutcomment)
  woutcomment_row.append(ed_Azure_lm_low_woutcomment)
  
  # Azure LM Medium
  Azure_lm_medium_wcomment = fmt_code(remove_blank_lines(raw_data['Azure LM Medium'][i])) # With Comments
  wcomment_row.append(Azure_lm_medium_wcomment)
  
  ed_Azure_lm_medium_wcomment = editdistance.eval(ground_truth, Azure_lm_medium_wcomment)
  wcomment_row.append(ed_Azure_lm_medium_wcomment)
  
  
  Azure_lm_medium_woutcomment = fmt_code(remove_blank_lines(remove_comments(Azure_lm_medium_wcomment))) # Without Comments
  woutcomment_row.append(Azure_lm_medium_woutcomment)
  
  ed_Azure_lm_medium_woutcomment = editdistance.eval(ground_truth_woutcomment, Azure_lm_medium_woutcomment)
  woutcomment_row.append(ed_Azure_lm_medium_woutcomment)
  
  # Azure LM High
  Azure_lm_high_wcomment = fmt_code(remove_blank_lines(raw_data['Azure LM High'][i])) # With Comments
  wcomment_row.append(Azure_lm_high_wcomment)
  
  ed_Azure_lm_high_wcomment = editdistance.eval(ground_truth, Azure_lm_high_wcomment)
  wcomment_row.append(ed_Azure_lm_high_wcomment)
  
  
  Azure_lm_high_woutcomment = fmt_code(remove_blank_lines(remove_comments(Azure_lm_high_wcomment))) # Without Comments
  woutcomment_row.append(Azure_lm_high_woutcomment)
  
  ed_Azure_lm_high_woutcomment = editdistance.eval(ground_truth_woutcomment, Azure_lm_high_woutcomment)
  woutcomment_row.append(ed_Azure_lm_high_woutcomment)
  
  # MP
  MP = raw_data['MP'][i]
  wcomment_row.append(MP)
  woutcomment_row.append(remove_blank_lines(remove_comments(MP)))
  
  ed_MP = raw_data['ED MP'][i]
  wcomment_row.append(ed_MP)
  ed_mp_woutcomment = editdistance.eval(ground_truth_woutcomment, remove_comments(MP))
  woutcomment_row.append(ed_mp_woutcomment)
  
  # MP LM Low
  MP_lm_low_wcomment = fmt_code(remove_blank_lines(raw_data['MP LM Low'][i])) # With Comments
  wcomment_row.append(MP_lm_low_wcomment)
  
  ed_MP_lm_low_wcomment = editdistance.eval(ground_truth, MP_lm_low_wcomment)
  wcomment_row.append(ed_MP_lm_low_wcomment)
  
  
  MP_lm_low_woutcomment = fmt_code(remove_blank_lines(remove_comments(MP_lm_low_wcomment))) # Without Comments
  woutcomment_row.append(MP_lm_low_woutcomment)
  
  ed_MP_lm_low_woutcomment = editdistance.eval(ground_truth_woutcomment, MP_lm_low_woutcomment)
  woutcomment_row.append(ed_MP_lm_low_woutcomment)
  
  # MP LM Medium
  MP_lm_medium_wcomment = fmt_code(remove_blank_lines(raw_data['MP LM Medium'][i])) # With Comments
  wcomment_row.append(MP_lm_medium_wcomment)
  
  ed_MP_lm_medium_wcomment = editdistance.eval(ground_truth, MP_lm_medium_wcomment)
  wcomment_row.append(ed_MP_lm_medium_wcomment)
  
  
  MP_lm_medium_woutcomment = fmt_code(remove_blank_lines(remove_comments(MP_lm_medium_wcomment))) # Without Comments
  woutcomment_row.append(MP_lm_medium_woutcomment)
  
  ed_MP_lm_medium_woutcomment = editdistance.eval(ground_truth_woutcomment, MP_lm_medium_woutcomment)
  woutcomment_row.append(ed_MP_lm_medium_woutcomment)
  
  # MP LM High
  MP_lm_high_wcomment = fmt_code(remove_blank_lines(raw_data['MP LM High'][i])) # With Comments
  wcomment_row.append(MP_lm_high_wcomment)
  
  ed_MP_lm_high_wcomment = editdistance.eval(ground_truth, MP_lm_high_wcomment)
  wcomment_row.append(ed_MP_lm_high_wcomment)
  
  
  MP_lm_high_woutcomment = fmt_code(remove_blank_lines(remove_comments(MP_lm_high_wcomment))) # Without Comments
  woutcomment_row.append(MP_lm_high_woutcomment)
  
  ed_MP_lm_high_woutcomment = editdistance.eval(ground_truth_woutcomment, MP_lm_high_woutcomment)
  woutcomment_row.append(ed_MP_lm_high_woutcomment)
  
  
  with open ('FINAL DATA/wcommentall.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(wcomment_row)
    
  with open ('FINAL DATA/woutcommentall.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(woutcomment_row)
    
  print('Done with row ' + str(i))