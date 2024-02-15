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


start = timeit.timeit()



gcloud_vision_client = vision.ImageAnnotatorClient.from_service_account_json("gcloud-sacct-cred.json")




def authenticate_gdrive():
    gauth = GoogleAuth()
    # Load client secrets from your key file 
    gauth.LoadClientConfigFile('credentials.json')
    return GoogleDrive(gauth)

DRIVE = authenticate_gdrive()

def download_file(DRIVE, id, image_path):
    # "1a2B3c4D5e6F" is the file id of the image file 
    file = DRIVE.CreateFile({'id': id}) 
    # This will replace the existing file with your file
    file.GetContentFile(image_path, mimetype='image/jpg')

main_data = pd.read_csv('errordata/Error Data V2023-08-10 - Sheet1.csv')


def fmt_code(code: str) -> str:
    try:
        return black.format_str(code, mode=black.FileMode())

    except InvalidInput as e:
        print(f"Invalid Python code: {e}")
        print(f"Code: {code}")
        return code

    except Exception as e:
        print(f"Unexpected error with Black auto-styling: {e}")
        print(f"Code: {code}")
        return code

# Preparing the CSV file

def prepare_csv():
    with open('errordata/derrorresults.csv', 'a', newline='') as csv_file:
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
    
prepare_csv()

GROUND_TRUTH_LIST = []
for i in range(45):
    GROUND_TRUTH_LIST.append(str(i))
    
for i in range(len(main_data['groundtruth'])):
    GROUND_TRUTH_LIST.append(clear_response(fmt_code(str(main_data['groundtruth'][i]))))

DATA_LST = []



for temperature in TEMPERATURES:
    print("Beginning the temperature: " + str(temperature))
    loop_start = 45
    for i in range(loop_start, 55):
        
        
        
        row = []
        print("\n|----------------------------------------------------------------------------|\n")
        print("This the image number: " + str(i))
        print("\n---------------------------------------------")
        print("---------------------------------------------\n")
        
        #Getting the ground truth
        print("This is the ground truth: \n" + GROUND_TRUTH_LIST[i])
        row.append(GROUND_TRUTH_LIST[i])
        
        row.append(temperature)
        
        # Getting the image id
        # link = data['imagelink'][i].split(',')[0].strip()
        # id_start = link.find('id=') + 3
        # id = link[id_start:]
        
        image_path = 'images/' + str(i) + '.jpg'
        # print("This is the id: \n" + str(id))
        
        # Not downloading the image if it already exists
        # download_file(DRIVE, id, image_path)
        
        
        """
        
        This is the part where we use Google Cloud Vision
        
        """
        
        
        print("\n---------------------------------------------\n")
        print("Google Cloud Vision Part")
        print("\n---------------------------------------------\n")

        GCV_response_text = GCV(image_path)
        
        
        # GCV_response_text = clean(GCV_response_text, normalize_whitespace=True) # Normalize the text
        
        print("This is the GCV response: \n \n" + str(GCV_response_text))
        row.append(GCV_response_text)
        
        print("This is the edit distance: " + str(editdistance.eval(GCV_response_text, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(GCV_response_text, GROUND_TRUTH_LIST[i]))
        time.sleep(2)
        
        print("\n|----------------------------------------------------------------------------|\n")
        # MP Low LM
        GCV_LM_response_low, GCV_LM_response_low_json = LM_correction_low(GCV_response_text, temperature)
        GCV_LM_response_low = clear_response(GCV_LM_response_low)
        
        time.sleep(2)
        # GCV_LM_response_low = clean(GCV_LM_response_low, normalize_whitespace=True) # Normalize the text
        GCV_LM_response_low = fmt_code(GCV_LM_response_low)
        
        print("This is the GCV LM response LOW: \n\n" + str(GCV_LM_response_low))
        row.append(GCV_LM_response_low)
        print("This is the edit distance: " + str(editdistance.eval(GCV_LM_response_low, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(GCV_LM_response_low, GROUND_TRUTH_LIST[i]))
        
        print("\n|----------------------------------------------------------------------------|\n")
        # GCV Medium LM
        GCV_LM_response_medium, GCV_LM_response_medium_json = LM_correction_medium(GCV_response_text, temperature)
        GCV_LM_response_medium = clear_response(GCV_LM_response_medium)
        
        time.sleep(2)
        # GCV_LM_response_medium = clean(GCV_LM_response_medium, normalize_whitespace=True) # Normalize the text
        GCV_LM_response_medium = fmt_code(GCV_LM_response_medium) # Formatting The Code
        
        
        print("This is the GCV LM response MEDIUM: \n\n" + str(GCV_LM_response_medium))
        row.append(GCV_LM_response_medium)
        print("This is the edit distance: " + str(editdistance.eval(GCV_LM_response_medium, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(GCV_LM_response_medium, GROUND_TRUTH_LIST[i]))
        
        print("\n|----------------------------------------------------------------------------|\n")
        # GCV High LM
        GCV_LM_response_high, GCV_LM_response_high_json = LM_correction_high(GCV_response_text, temperature)
        GCV_LM_response_high = clear_response(GCV_LM_response_high)
        
        time.sleep(2)
        # GCV_LM_response_high = clean(GCV_LM_response_high, normalize_whitespace=True) # Normalize the text
        GCV_LM_response_high = fmt_code(GCV_LM_response_high) # Formatting The Code
        
        print("This is the GCV LM response HIGH: \n\n" + str(GCV_LM_response_high))
        row.append(GCV_LM_response_high)
        print("This is the edit distance: " + str(editdistance.eval(GCV_LM_response_high, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(GCV_LM_response_high, GROUND_TRUTH_LIST[i]))
        print("\n|----------------------------------------------------------------------------|\n")
        
        
        
        """
        
        This is the part where we use AWS Textract
        
        """
        print("\n---------------------------------------------\n")
        print("Amazon Web Services Textract Part")
        print("\n---------------------------------------------\n")
        
        AWS_response_text = AWS_textract(image_path)
        
        # AWS_response_text = clean(AWS_response_text, normalize_whitespace=True) # Normalize the text
        
        print("This is the AWS response: \n\n" + str(AWS_response_text))
        row.append(AWS_response_text)
        
        print("This is the edit distance: " + str(editdistance.eval(AWS_response_text, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(AWS_response_text, GROUND_TRUTH_LIST[i]))
        time.sleep(2)
        
        print("\n|----------------------------------------------------------------------------|\n")
        # MP Low LM
        AWS_LM_response_low, AWS_LM_response_low_json = LM_correction_low(AWS_response_text, temperature)
        AWS_LM_response_low = clear_response(AWS_LM_response_low)
        
        time.sleep(2)
        # AWS_LM_response_low = clean(AWS_LM_response_low, normalize_whitespace=True) # Normalize the text
        AWS_LM_response_low = fmt_code(AWS_LM_response_low)
        
        print("This is the AWS LM response LOW: \n\n" + str(AWS_LM_response_low))
        row.append(AWS_LM_response_low)
        print("This is the edit distance: " + str(editdistance.eval(AWS_LM_response_low, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(AWS_LM_response_low, GROUND_TRUTH_LIST[i]))
        
        print("\n|----------------------------------------------------------------------------|\n")
        # AWS Medium LM
        AWS_LM_response_medium, AWS_LM_response_medium_json = LM_correction_medium(AWS_response_text, temperature)
        AWS_LM_response_medium = clear_response(AWS_LM_response_medium)
        
        time.sleep(2)
        # AWS_LM_response_medium = clean(AWS_LM_response_medium, normalize_whitespace=True) # Normalize the text
        AWS_LM_response_medium = fmt_code(AWS_LM_response_medium) # Formatting The Code
        
        
        print("This is the AWS LM response MEDIUM: \n\n" + str(AWS_LM_response_medium))
        row.append(AWS_LM_response_medium)
        print("This is the edit distance: " + str(editdistance.eval(AWS_LM_response_medium, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(AWS_LM_response_medium, GROUND_TRUTH_LIST[i]))
        
        print("\n|----------------------------------------------------------------------------|\n")
        # AWS High LM
        AWS_LM_response_high, AWS_LM_response_high_json = LM_correction_high(AWS_response_text, temperature)
        AWS_LM_response_high = clear_response(AWS_LM_response_high)
        
        time.sleep(2)
        # AWS_LM_response_high = clean(AWS_LM_response_high, normalize_whitespace=True) # Normalize the text
        AWS_LM_response_high = fmt_code(AWS_LM_response_high) # Formatting The Code
        
        print("This is the AWS LM response HIGH: \n\n" + str(AWS_LM_response_high))
        row.append(AWS_LM_response_high)
        print("This is the edit distance: " + str(editdistance.eval(AWS_LM_response_high, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(AWS_LM_response_high, GROUND_TRUTH_LIST[i]))
        print("\n|----------------------------------------------------------------------------|\n")
        
        
        
        
        """
        
        This is the Part where we use Azure
        
        """
        print("\n---------------------------------------------\n")
        print("Microsoft Azure Part")
        print("\n---------------------------------------------\n")
        
        Azure_response_text = azure(image_path)
        
        # Azure_response_text = clean(Azure_response_text, normalize_whitespace=True) # Normalize the text
        
        print("This is the Azure response: \n\n" + str(Azure_response_text))
        row.append(Azure_response_text)
        
        print("This is the edit distance: " + str(editdistance.eval(Azure_response_text, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(Azure_response_text, GROUND_TRUTH_LIST[i]))
        time.sleep(2)
        
        print("\n|----------------------------------------------------------------------------|\n")
        # MP Low LM
        Azure_LM_response_low, Azure_LM_response_low_json = LM_correction_low(Azure_response_text, temperature)
        Azure_LM_response_low = clear_response(Azure_LM_response_low)
        
        time.sleep(2)
        # Azure_LM_response_low = clean(Azure_LM_response_low, normalize_whitespace=True) # Normalize the text
        Azure_LM_response_low = fmt_code(Azure_LM_response_low)
        
        print("This is the Azure LM response LOW: \n\n" + str(Azure_LM_response_low))
        row.append(Azure_LM_response_low)
        print("This is the edit distance: " + str(editdistance.eval(Azure_LM_response_low, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(Azure_LM_response_low, GROUND_TRUTH_LIST[i]))
        
        print("\n|----------------------------------------------------------------------------|\n")
        # Azure Medium LM
        Azure_LM_response_medium, Azure_LM_response_medium_json = LM_correction_medium(Azure_response_text, temperature)
        Azure_LM_response_medium = clear_response(Azure_LM_response_medium)
        
        time.sleep(2)
        # Azure_LM_response_medium = clean(Azure_LM_response_medium, normalize_whitespace=True) # Normalize the text
        Azure_LM_response_medium = fmt_code(Azure_LM_response_medium) # Formatting The Code
        
        
        print("This is the Azure LM response MEDIUM: \n\n" + str(Azure_LM_response_medium))
        row.append(Azure_LM_response_medium)
        print("This is the edit distance: " + str(editdistance.eval(Azure_LM_response_medium, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(Azure_LM_response_medium, GROUND_TRUTH_LIST[i]))
        
        print("\n|----------------------------------------------------------------------------|\n")
        # Azure High LM
        Azure_LM_response_high, Azure_LM_response_high_json = LM_correction_high(Azure_response_text, temperature)
        Azure_LM_response_high = clear_response(Azure_LM_response_high)
        
        time.sleep(2)
        # Azure_LM_response_high = clean(Azure_LM_response_high, normalize_whitespace=True) # Normalize the text
        Azure_LM_response_high = fmt_code(Azure_LM_response_high) # Formatting The Code
        
        print("This is the Azure LM response HIGH: \n\n" + str(Azure_LM_response_high))
        row.append(Azure_LM_response_high)
        print("This is the edit distance: " + str(editdistance.eval(Azure_LM_response_high, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(Azure_LM_response_high, GROUND_TRUTH_LIST[i]))
        print("\n|----------------------------------------------------------------------------|\n")
        
        
        
        
        """
        
        This is the Part where we use Mathpix
        
        """
        print("\n---------------------------------------------\n")
        print("Mathpix Part")
        print("\n---------------------------------------------\n")
        

        MP_response = mathpix(image_path)
        if MP_response == None:
            print("Trying Mathpix again")
            MP_response = mathpix(image_path)
            if MP_response == None:
                MP_response = "The API did not work, look above for the error"
        else:
            MP_response_text = MP_response['text']
        
        time.sleep(2)
        # MP_response_text = clean(MP_response_text, normalize_whitespace=True) # Normalize the text
        
        print("This is the MP response: \n\n" + str(MP_response_text))
        row.append(MP_response_text)
        print("This is the edit distance: " + str(editdistance.eval(MP_response_text, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(MP_response_text, GROUND_TRUTH_LIST[i]))
        
        
        #Processing the text
        if MP_response == "The API did not work, look above for the error":
            source_code = MP_response
        else:
            min_x, labels, data = cluster_indentation(MP_response)
            source_code, data = process_indentation(data)
            
            
        print("\n|----------------------------------------------------------------------------|\n")
        # MP Low LM
        MP_LM_response_low, MP_LM_response_low_json = LM_correction_low(source_code, temperature)
        MP_LM_response_low = clear_response(MP_LM_response_low)
        
        time.sleep(2)
        # MP_LM_response_low = clean(MP_LM_response_low, normalize_whitespace=True) # Normalize the text
        MP_LM_response_low = fmt_code(MP_LM_response_low)
        
        print("This is the Mathpix LM response LOW: \n\n" + str(MP_LM_response_low))
        row.append(MP_LM_response_low)
        print("This is the edit distance: " + str(editdistance.eval(MP_LM_response_low, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(MP_LM_response_low, GROUND_TRUTH_LIST[i]))
        
        print("\n|----------------------------------------------------------------------------|\n")
        # MP Medium LM
        MP_LM_response_medium, MP_LM_response_medium_json = LM_correction_medium(source_code, temperature)
        MP_LM_response_medium = clear_response(MP_LM_response_medium)
        
        time.sleep(2)
        # MP_LM_response_medium = clean(MP_LM_response_medium, normalize_whitespace=True) # Normalize the text
        MP_LM_response_medium = fmt_code(MP_LM_response_medium) # Formatting The Code
        
        
        print("This is the Mathpix LM response MEDIUM: \n\n" + str(MP_LM_response_medium))
        row.append(MP_LM_response_medium)
        print("This is the edit distance: " + str(editdistance.eval(MP_LM_response_medium, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(MP_LM_response_medium, GROUND_TRUTH_LIST[i]))
        
        print("\n|----------------------------------------------------------------------------|\n")
        
        # MP High LM
        MP_LM_response_high, MP_LM_response_high_json = LM_correction_high(source_code, temperature)
        MP_LM_response_high = clear_response(MP_LM_response_high)
        
        time.sleep(2)
        # MP_LM_response_high = clean(MP_LM_response_high, normalize_whitespace=True) # Normalize the text
        MP_LM_response_high = fmt_code(MP_LM_response_high) # Formatting The Code
        
        print("This is the Mathpix LM response HIGH: \n\n" + str(MP_LM_response_high))
        row.append(MP_LM_response_high)
        print("This is the edit distance: " + str(editdistance.eval(MP_LM_response_high, GROUND_TRUTH_LIST[i])))
        row.append(editdistance.eval(MP_LM_response_high, GROUND_TRUTH_LIST[i]))
        print("\n|----------------------------------------------------------------------------|\n")
        


        
        # The Final Part
        with open('errordata/derrorresults.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(row)
            print("This is the row: " + str(i))
        
        print("\n|----------------------------------------------------------------------------|\n")
        print("End of the temperature " + str(temperature), "row: " + str(i))
        print("\n|----------------------------------------------------------------------------|\n")
        print("Waiting 30 seconds for the next image.....")
        # time.sleep(30)

        # Previous Approach
        # DATA_LST.append(row)
        
        
        # print(DATA_LST)




end = time.time()

print("This is the time taken: " + str(end - start))