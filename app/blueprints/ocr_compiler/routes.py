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
import base64

load_dotenv()
gcloud_vision_client = vision.ImageAnnotatorClient.from_service_account_json("keys/gcloud-sacct-cred.json")

print("Outside the function")
print(os.getenv("OPENAI_KEY"))

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
        
        source_code, annotated_image = ocr_code(file_path)
        
        print(" ")
        print("Below is the source to the subject image:")
        print(code_picture)
        return render_template(
            "index.html",
            source_code=source_code,
            code_picture=code_picture,
            annotated_image=annotated_image,
        )

def ocr_code(image_path):
    with open(image_path, "rb") as img_file:
        file_content = img_file.read()
    image = vision.Image(content=file_content)
    response = gcloud_vision_client.document_text_detection(image=image)
    source_code = response.full_text_annotation.text

    # Call the annotate_image function
    annotated_image = annotate_image(str(image_path), response)  # Convert the image_path to a string

    # Return both source_code and annotated_image
    return source_code, annotated_image

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