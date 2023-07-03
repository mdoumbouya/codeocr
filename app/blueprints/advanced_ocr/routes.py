# app/blueprints/ocr_compiler/routes.py

from flask import render_template, request, current_app
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from google.cloud import vision
import uuid
from flask import jsonify
from dotenv import load_dotenv
from app.blueprints.advanced_ocr import bp

from app.global_utils import *
import requests
import base64
import openai 

import json

import io
import contextlib


load_dotenv()

MATHPIX_APP_ID = os.getenv("MATHPIX_APP_ID")
MATHPIX_APP_KEY = os.getenv("MATHPIX_APP_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

print("Open AI KEY TEST")

print("OPENAI_API_KEY:", OPENAI_API_KEY)

@bp.route("/advanced", methods=["GET", "POST"])
def advanced():
    if request.method == 'GET':
        return render_template("advanced_index.html")
    else:
        print("Inside the function")
        print(os.getenv("OPENAI_KEY"))
        file = request.files["code_picture"]
        filename = str(uuid.uuid4()) + secure_filename(file.filename)
        file_path = Path(current_app.config['UPLOAD_FOLDER']) / filename
        file.save(file_path)
        code_picture = os.path.join("..", "static", "uploaded_images", filename)
        
        source_code, histogram, clustering, visualized_lines = ocr_code(file_path)
        
        mathpix_output = source_code
        
        # source_code = clear_response(language_model_correction(source_code))
        
        # test = final_processing(source_code)
        
        
        
        print(" ")
        print("Below is the source to the subject image:")
        print(code_picture)
        return render_template(
            "advanced_index.html",
            source_code=source_code,
            code_picture=code_picture,
            histogram=Markup(histogram),
            clustering=Markup(clustering),
            visualized_lines=visualized_lines,
            mathpix_output=mathpix_output,
        )


def ocr_code(image_path):
    with open(image_path, "rb") as img_file:
        image_data = img_file.read()
        
    b64_image = base64.b64encode(image_data).decode("utf-8")
    
    headers = {
        "app_id": MATHPIX_APP_ID,
        "app_key": MATHPIX_APP_KEY,
        "Content-type": "application/json",
    }
    
    data = {
    "src": "data:image/jpeg;base64," + b64_image,
    "formats": ["text"],
    "include_line_data": True
    }
    
    response = requests.post("https://api.mathpix.com/v3/text", json=data, headers=headers)
    
    if response.status_code == 200:
        json_response = response.json()
        min_x, labels, data = cluster_indentation(json_response)
        print("Printing the initial form of data")
        for elem in data:
            if elem == "line_data":
                for ix, line in enumerate(data[elem]):
                    print("")
                    print(ix + 1)
                
                    print(line)
            else:
                print(data[elem])
        
        source_code, data = process_indentation(data)
        histogram = plot_histogram(min_x)
        clustering = plot_clustering(min_x, labels)
        visualized_lines = visualize_lines(data, image_path=str(image_path))
        print("Printing the final form of data")
        for elem in data:
            if elem == "line_data":
                for ix, line in enumerate(data[elem]):
                    print("")
                    print(ix + 1)
                
                    print(line)
            else:
                print(data[elem])
            
    else:
        source_code = ""
        histogram = ""
        clustering = ""
        visualized_lines = ""
        
    
    return source_code, histogram, clustering, visualized_lines



def language_model_correction(input_text):
    print("Into the post process gpt function")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who helps translate result of handwritten python code from Mathpix API to Python code.",
        },
        {
            "role": "user",
            "content": f"This is an cleaned output of mathpix API, which outputs latex from an image of handwriting. This is the output it provided from a handwritten code: {input_text}",
        },
        {
            "role": "user",
            "content": "Fix all sorts of typos in the code, inluding the string; Just fix all the mistakes that a OCR engine can make.",
        },
        {
            "role": "user",
            "content": "return exactly the same number of lines as the input, including comments in python code, and do not change the order of the lines, or increase the number of lines.",
        },
        {
            "role": "user",
            "content": "keep the code layout exactly as it is, do not tamper with the indentation",
        },
    ]

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    payload = {
        "model": "gpt-4-0613",
        "messages": messages,
        "max_tokens": 2042,
    }

    try:
        print("trying GPT")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("GPT worked")
            response_json = response.json()
            print(response_json)
            result = response_json["choices"][0]["message"]["content"].strip()
            return result
        else:
            print("GPT failed")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""





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