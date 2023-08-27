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
from global_utils import *
import base64
from cleantext import clean
import black
from black import InvalidInput
import timeit


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
from global_utils import *
import base64
from cleantext import clean
import black
from black import InvalidInput
import timeit


start = timeit.timeit()



gcloud_vision_client = vision.ImageAnnotatorClient.from_service_account_json("gcloud-sacct-cred.json")



main_data = pd.read_csv('errordata/Error Data V2023-08-10 - Sheet1.csv')

# Preparing the CSV file

def prepare_csv():
    with open('errordata/derrorresults.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # write the header
        writer.writerow(['Ground Truth',
                            'GCV',
                            'ED GCV',
                            'GCV LM', 
                            'ED GCV LM', 
                            'AWS', # AWS Starts Here
                            'ED AWS',
                            'AWS LM',
                            'ED AWS LM',
                            'Azure', # Azure Starts Here
                            'ED Azure',
                            'Azure LM', 
                            'ED Azure LM', 
                            'MP', # Mathpix Starts Here
                            'ED MP', 
                            'MP LM',
                            'ED MP LM',
                            ])
    
prepare_csv()

GROUND_TRUTH_LIST = []
for i in range(45):
    GROUND_TRUTH_LIST.append(str(i))
    
for i in range(len(main_data['groundtruth'])):
    GROUND_TRUTH_LIST.append(clear_response(fmt_code(str(main_data['groundtruth'][i]))))

DATA_LST = []



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
  