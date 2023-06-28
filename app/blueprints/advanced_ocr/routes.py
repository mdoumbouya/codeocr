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
        
        source_code = hard_postprocess(language_model_correction(source_code))
        
        
        
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
        source_code = json_response.get("text", "")
        
        min_x, labels, data = cluster_indentation(json_response)
        histogram = plot_histogram(min_x)
        clustering = plot_clustering(min_x, labels)
        visualized_lines = visualize_lines(data, image_path=str(image_path))
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
            "content": "You are a helpful assistant who helps translate Python in latex to Python code.",
        },
        {
            "role": "user",
            "content": f"This is an output of matrix API, which outputs latex from an image of handwriting. This is the output it provided from a handwritten code: {input_text}",
        },
        {
            "role": "user",
            "content": "Fix the typos in Python text; however, don't do anything about the indentation. Just go to a new line at every \\n. Fix typos in strings, or vars name inside text. Dont return anything else tha n the corrected Python text, as in dont return any preceding text, or return any ending text, return JUST THE Python Code",
        },
    ]

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    payload = {
        "model": "gpt-4",
        "messages": messages,
        "max_tokens": 2042,
    }

    try:
        print("trying GPT")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("GPT worked")
            response_json = response.json()
            result = response_json["choices"][0]["message"]["content"].strip()
            return result
        else:
            print("GPT failed")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""


def hard_postprocess(txt):
    print(txt)
    first_tilda = txt.find("```")
    print("first_tilda", first_tilda)
    if first_tilda != -1:
        second_tilda = txt.find("```", first_tilda + 1)
        print("second_tilda", second_tilda)
        if second_tilda != -1:
            print("Checking the string after the first tilda")
            print(txt[first_tilda + 3: first_tilda + 9])
            if txt[first_tilda + 3: first_tilda + 9] == "python":
                return txt[first_tilda + 9:second_tilda]
            else:
                return txt[first_tilda + 3:second_tilda]



@bp.route('/run_code', methods=['POST'])
def run_code():
    source_code = request.form.get('source_code')
    code_picture = request.form.get('code_picture')
    try:
        exec_globals = {}
        exec_locals = {}
        exec(source_code, exec_globals, exec_locals)
        compilation_results = exec_locals
        return jsonify({"compilation_results": str(compilation_results), "source_code": source_code, "code_picture": code_picture})

    except Exception as e:
        compilation_results = str(e)
        return jsonify({"compilation_results": compilation_results, "source_code": source_code, "code_picture": code_picture})