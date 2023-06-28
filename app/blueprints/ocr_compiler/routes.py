# app/blueprints/ocr_compiler/routes.py

from flask import render_template, request, current_app
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from google.cloud import vision
import uuid
from flask import jsonify
from dotenv import load_dotenv
from app.blueprints.ocr_compiler import bp

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

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        print("Inside the function")
        print(os.getenv("OPENAI_KEY"))
        file = request.files["code_picture"]
        filename = str(uuid.uuid4()) + secure_filename(file.filename)
        file_path = Path(current_app.config['UPLOAD_FOLDER']) / filename
        file.save(file_path)
        code_picture = os.path.join("..", "static", "uploaded_images", filename)
        
        source_code = ocr_code(file_path)
        
        source_code = post_process_output(source_code)
        
        print(" ")
        print("Below is the source to the subject image:")
        print(code_picture)
        return render_template(
            "index.html",
            source_code=source_code,
            code_picture=code_picture,
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
        "formats": ["text", "data"],
        "data_options": {
            "include_asciimath": True
        },
        "include_line_data": True
    }
    
    response = requests.post("https://api.mathpix.com/v3/text", json=data, headers=headers)
    
    if response.status_code == 200:
        json_response = response.json()
        source_code = json_response.get("text", "")
    else:
        source_code = ""
    
    return source_code



def post_process_output(input_text):
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
            "content": "Fix the typos in Python text; however, don't do anything about the indentation. Just go to a new line at every \\n. Fix typos in strings, or vars name inside text. Dont return anything else the corrected Python text, as in dont return any preceding text, or return any ending text, JUST THE Python Code",
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