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