# app/blueprints/ocr_compiler/routes.py

from flask import render_template, request, current_app
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import uuid
from flask import jsonify
from dotenv import load_dotenv
from app.blueprints.advanced_ocr import bp

from code_ocr.global_utils import *
import requests
import base64
import openai 

import json

import io
import contextlib
from timeit import default_timer as timer

from code_ocr.indentation_recognition import MeanShiftIndentRecognitionAlgo, GaussianIndentationRecognitionAlgo
from code_ocr.post_correction import COTprompting, SIMPLEprompting, SIMPLEprompting_test2

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import session

load_dotenv()

MATHPIX_APP_ID = os.getenv("MATHPIX_APP_ID")
MATHPIX_APP_KEY = os.getenv("MATHPIX_APP_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Use the application default credentials
cred = credentials.Certificate('firebase_credentials.json')
# firebase_admin.initialize_app(cred)

db = firestore.client()


@bp.route("/advanced", methods=["GET", "POST"])
def advanced():
    if request.method == 'GET':
        return render_template("advanced_index.html")
    else:
        
        start_time = timer()
        print("Inside the basic page function")
        file = request.files["code_picture"]
        filename = str(uuid.uuid4()) + secure_filename(file.filename)
        image_path = Path(current_app.config['UPLOAD_FOLDER']) / filename
        file.save(image_path)
        image_path = str(image_path)
        

        code_picture = upload_image(image_path, filename)

        
        
        
        """
        Change Mathpix to Azure here, using the latest azure implementation with Moussa
        """
        # Sending the image to Microsoft Azure
        ocr_start_time = timer()
        json_OCRresponse = azure_payload(image_path)
        # print("json_OCRresponse: \n", json_OCRresponse)
        # print("----------------------------------------------")
        ocr_end_time = timer()
        
        
        
        # Getting the gneralized form of line data using the new method
        document_metadata = line_data(json_OCRresponse)
        
        image = cv2.imread(image_path)
        image_height, image_width, _ = image.shape
        
        document_metadata["image_height"] = image_height
        document_metadata["image_width"] = image_width
        
        # print("lines_data: \n", document_metadata)
        # print("----------------------------------------------")
        
        ir_output = MeanShiftIndentRecognitionAlgo(bandwidth="estimated").recognize_indents(document_metadata)
        
        # print("ir_output: \n", ir_output)
        # print("----------------------------------------------")
        
        
        min_x = []
        labels = []
        
        # print("ir_output: ", ir_output['ir_algo_output_indented_lines'])
        
        for line in ir_output['ir_algo_output_indented_lines']:
            min_x.append(line['x'])
            labels.append(line['cluster_label'])
            
            
        # print("labels: ", labels)
        # min_x, labels, data = cluster_indentation(json_MPresponse)
        # source_code, data = process_indentation(data)
        raw_azure_output = ''
        
        for line in document_metadata['ocr_ouptut']:
            raw_azure_output += line['text'] + '\n'
        
        
        histogram = plot_histogram(min_x)
        clustering = plot_clustering(min_x, labels)

        ocr_output = raw_azure_output
        
        visualized_lines = draw_lines(image_path, ir_output)
        retval, buffer = cv2.imencode('.jpg', visualized_lines)
        final_visualized_lines = base64.b64encode(buffer).decode('utf-8')
        
        json_LMresponse = None # Adding this just for the time being, plan on adding the json response from LM down the way
        source_code = SIMPLEprompting_test2().post_correction(ir_output)

        
        # print("source_code: ", source_code)
        
        source_code = remove_blank_lines(clear_response(source_code))
        
        storing_start = timer()
        doc_ref = db.collection('codeocr').document() 
        doc_ref.set({
            'id': doc_ref.id,        
            'image_url': code_picture,
            'ocr_response': json.dumps(json_OCRresponse),
            'language_model_response': json.dumps(json_LMresponse),
            'source_code': source_code,
            'lm_intensity': 'simple',
        })
        
        session['doc_id'] = doc_ref.id
        storing_end = timer()
        

        if os.path.exists(image_path):
            # Delete the file
            os.remove(image_path)
            
        
        return render_template(
            "advanced_index.html",
            source_code=source_code,
            code_picture=code_picture,
            histogram=Markup(histogram),
            clustering=Markup(clustering),
            visualized_lines=final_visualized_lines,
            ocr_output=ocr_output,
        )




@bp.route('/run_code', methods=['POST'])
def run_code():
    source_code = request.form.get('source_code')
    code_picture = request.form.get('code_picture')

    # create a StringIO object to capture stdout
    stdout = io.StringIO()

    try:
        # Redirect stdout to the StringIO object
        with contextlib.redirect_stdout(stdout):
            exec(source_code)

        # Get the stdout value from StringIO object
        compilation_results = stdout.getvalue()

        return jsonify({"compilation_results": compilation_results, 
                        "source_code": source_code, 
                        "code_picture": code_picture})

    except Exception as e:
        compilation_results = str(e)
        return jsonify({"compilation_results": compilation_results, 
                        "source_code": source_code, 
                        "code_picture": code_picture})
        
        
        
DOT_COLORS =  [
    ((0, 0, 255), 'rgb(255, 0, 0)'),       # red
    ((0, 255, 0), 'rgb(0, 255, 0)'),       # green
    ((255, 0, 0), 'rgb(0, 0, 255)'),       # blue
    ((255, 0, 255), 'rgb(255, 0, 255)'),   # magenta
    ((192, 255, 0), 'rgb(0, 255, 192)'),   # mint green
    ((64, 0, 255), 'rgb(255, 0, 64)'),     # deep pink
    ((128, 255, 255), 'rgb(255, 255, 128)'), # pastel yellow
    ((128, 255, 128), 'rgb(128, 255, 128)'), # pastel green
    ((255, 255, 128), 'rgb(128, 255, 255)'), # pastel cyan
    ((255, 255, 0), 'rgb(0, 255, 255)'),   # cyan
    ((255, 165, 0), 'rgb(0, 165, 255)'),   # orange
    ((255, 105, 180), 'rgb(180, 105, 255)'), # hot pink
    ((255, 64, 0), 'rgb(0, 64, 255)'),     # deep orange
    ((0, 165, 255), 'rgb(255, 165, 0)'),   # light blue
    ((60, 179, 113), 'rgb(113, 179, 60)'), # medium sea green
    ((238, 130, 238), 'rgb(238, 130, 238)'), # violet
    ((245, 222, 179), 'rgb(179, 222, 245)'), # wheat
    ((210, 105, 30), 'rgb(30, 105, 210)'), # chocolate
    ((127, 255, 0), 'rgb(0, 255, 127)'),   # chartreuse
    ((255, 140, 0), 'rgb(0, 140, 255)'),   # dark orange
    ((32, 178, 170), 'rgb(170, 178, 32)'), # light sea green
]


# Drawing function
def draw_lines(image_path, data):
    # Load the image
    img = cv2.imread(image_path)
    img_dimensions = img.shape
    img_height = img_dimensions[0]
    img_width = img_dimensions[1]

    #Optimising the line thickness and dot radius based on the image size.
    min_dimension = min(img_height, img_width)
    line_thickness = max(min_dimension // 400, 1)
    text_offset = (img_width // 200) * 4 # This is the offset of the text from the dot
    dot_radius = line_thickness * 5
    
    # Draw lines based on OCR output
    for line in data["ocr_ouptut"]:
        x, y, w, h = line["x"], line["y"], line["w"], line["h"]
        top_left = (int(x), int(y))
        bottom_right = (int(x + w), int(y + h))
        cv2.rectangle(img, top_left, bottom_right, (255, 0, 0), line_thickness)

    # Map cluster labels to colors
    color_map = {i: color[0] for i, color in enumerate(DOT_COLORS)}

    # Draw a dot for each cluster label
    if "ir_algo_output_indented_lines" in data:
        for line in data["ir_algo_output_indented_lines"]:
            x, y = line["x"], line["y"]
            cluster_label = line["cluster_label"]
            cv2.circle(img, (int(x), int(y)), dot_radius, color_map[cluster_label % len(color_map)], -1) # Now it wraps around

            # Position of the text
            text_position = (int(x - text_offset), int(y))  # or any other position you prefer
            
            font_scale = max(0.5, min(img_height, img_width) / 700)  # change the divisible to any value that makes the font size look good

            # Other text properties
            font = cv2.FONT_HERSHEY_SIMPLEX  # or any other font
            font_color = (0, 255, 0)  # or any other color
            line_type = 2  # thickness of the line 
            cv2.putText(img, str(cluster_label), text_position, font, font_scale, font_color, line_type)
            
    return img