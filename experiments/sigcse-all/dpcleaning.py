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



raw_data = pd.read_csv('FINAL DATA/doubleprompted.csv')

    
def prepare_dp_csv(filename):
    with open(filename, 'a', newline='') as csv_file:
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


prepare_dp_csv('FINAL DATA/dpwcomment.csv')
prepare_dp_csv('FINAL DATA/dpwoutcomment.csv')

# prepare_csv('FINAL DATA/wcommentall.csv')
# prepare_csv('FINAL DATA/woutcommentall.csv')
    
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
  
  
  
  # GCV DP
  gcv_DP_wcomment = fmt_code(remove_blank_lines(raw_data['GCV DP'][i])) # With Comments
  wcomment_row.append(gcv_DP_wcomment)
  
  ed_gcv_DP_wcomment = editdistance.eval(ground_truth, gcv_DP_wcomment)
  wcomment_row.append(ed_gcv_DP_wcomment)
  
  
  gcv_DP_woutcomment = fmt_code(remove_blank_lines(remove_comments(gcv_DP_wcomment))) # Without Comments
  woutcomment_row.append(gcv_DP_woutcomment)
  
  ed_gcv_DP_woutcomment = editdistance.eval(ground_truth_woutcomment, gcv_DP_woutcomment)
  woutcomment_row.append(ed_gcv_DP_woutcomment)
  
  
  # AWS DP
  AWS_DP_wcomment = fmt_code(remove_blank_lines(raw_data['AWS DP'][i])) # With Comments
  wcomment_row.append(AWS_DP_wcomment)
  
  ed_AWS_DP_wcomment = editdistance.eval(ground_truth, AWS_DP_wcomment)
  wcomment_row.append(ed_AWS_DP_wcomment)
  
  
  AWS_DP_woutcomment = fmt_code(remove_blank_lines(remove_comments(AWS_DP_wcomment))) # Without Comments
  woutcomment_row.append(AWS_DP_woutcomment)
  
  ed_AWS_DP_woutcomment = editdistance.eval(ground_truth_woutcomment, AWS_DP_woutcomment)
  woutcomment_row.append(ed_AWS_DP_woutcomment)
  
  
  # Azure DP
  Azure_DP_wcomment = fmt_code(remove_blank_lines(raw_data['Azure DP'][i])) # With Comments
  wcomment_row.append(Azure_DP_wcomment)
  
  ed_Azure_DP_wcomment = editdistance.eval(ground_truth, Azure_DP_wcomment)
  wcomment_row.append(ed_Azure_DP_wcomment)
  
  
  Azure_DP_woutcomment = fmt_code(remove_blank_lines(remove_comments(Azure_DP_wcomment))) # Without Comments
  woutcomment_row.append(Azure_DP_woutcomment)
  
  ed_Azure_DP_woutcomment = editdistance.eval(ground_truth_woutcomment, Azure_DP_woutcomment)
  woutcomment_row.append(ed_Azure_DP_woutcomment)
  

  # MP DP
  MP_DP_wcomment = fmt_code(remove_blank_lines(raw_data['MP DP'][i])) # With Comments
  wcomment_row.append(MP_DP_wcomment)
  
  ed_MP_DP_wcomment = editdistance.eval(ground_truth, MP_DP_wcomment)
  wcomment_row.append(ed_MP_DP_wcomment)
  
  
  MP_DP_woutcomment = fmt_code(remove_blank_lines(remove_comments(MP_DP_wcomment))) # Without Comments
  woutcomment_row.append(MP_DP_woutcomment)
  
  ed_MP_DP_woutcomment = editdistance.eval(ground_truth_woutcomment, MP_DP_woutcomment)
  woutcomment_row.append(ed_MP_DP_woutcomment)
  
  
  
  with open ('FINAL DATA/dpwcomment.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(wcomment_row)
    
  with open ('FINAL DATA/dpwoutcomment.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(woutcomment_row)