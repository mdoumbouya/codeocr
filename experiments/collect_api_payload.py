"""
import pandas as pd
import time
import json
from global_utils import *


def prepare_dataframe():
    # Prepare dataframe with columns
    df = pd.DataFrame(columns=['GCV', 'AWS', 'Azure', 'MP'])
    return df

df = prepare_dataframe()
print("Dataframe created")

for i in range(55):
    print("This is the row: " + str(i))
    
    image_path = 'images/' + str(i) + '.jpg'
  
    # Google Cloud Vision
    GCV = GCV_payload(image_path)
  
    #AWS
    AWS = AWS_textract_payload(image_path)
  
    # Azure
    Azure = azure_payload(image_path)
  
    #Mathpix
    MP = mathpix_payload(image_path)
  
    # Append results to dataframe
    df.loc[len(df.index)] = [json.dumps(GCV), json.dumps(AWS), json.dumps(Azure), json.dumps(MP)]
    
  
    print("end of loop", str(i))

# Finally, save the dataframe to CSV
df.to_csv('apipayload.csv', index=False)

"""



# The way that works

"""
from global_utils import *
import csv
import pandas as pd
import time

def prepare_csv():
    with open('apipayload.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # write the header
        writer.writerow(['GCV',
                          'AWS',
                          'Azure',
                          'MP'
                            ])
    
prepare_csv()




for i in range(55):
  image_path = 'images/' + str(i) + '.jpg'
  
  row = []
  
  # Google Cloud Vision
  GCV = GCV_payload(image_path)
  row.append(GCV)
  
  #AWS
  AWS = AWS_textract_payload(image_path)
  row.append(AWS)
  
  # Azure
  Azure = azure_payload(image_path)
  row.append(Azure)
  
  #Mathpix
  MP = mathpix_payload(image_path)
  row.append(MP)
  
  with open('apipayload.csv', 'a', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(row)
    print("This is the row: " + str(i))
  

"""


"""


import requests
import json
import pandas as pd

response = requests.get('url_of_the_api')
data = response.json()   # data is a dictionary


# Assuming df is your DataFrame and 'api_results' is the column where you want to store the results
df = pd.DataFrame(columns=['api_results'])

# Convert the dictionary to a JSON formatted string before adding to the DataFrame
df.loc[len(df.index)] = [json.dumps(data)]   # Add the JSON string to the DataFrame


# Use .apply() with json.loads to convert the JSON strings back to dictionaries
df['api_results'] = df['api_results'].apply(json.loads)

# Now, df['api_results'] contains dictionaries

df.to_csv('filename.csv', index=False)


# When you read this CSV again, remember to apply `json.loads` again to convert the JSON string back to dictionary for further processing.

"""


# New Json way of doing it
import json
from code_ocr.global_utils import *

data = []
for i in range(55):
  image_path = 'images/' + str(i) + '.jpg'
  
  row = {}
  
  row['image_id'] = i
  # Google Cloud Vision
  GCV = GCV_payload(image_path)
  row['GCV'] = GCV
  
  #AWS
  AWS = AWS_textract_payload(image_path)
  row['AWS'] = AWS
  
  # Azure
  Azure = azure_payload(image_path)
  row['Azure'] = Azure
  
  #Mathpix
  MP = mathpix_payload(image_path)
  row['MP'] = MP
  
  print("This is the row: " + str(i))
  data.append(row)

with open('apipayload.json', 'w') as json_file:
    json.dump(data, json_file)