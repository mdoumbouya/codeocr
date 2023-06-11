# app/blueprints/ocr_compiler/routes.py

from flask import render_template, request, current_app
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from google.cloud import vision
import uuid

from app.blueprints.ocr_compiler import bp

gcloud_vision_client = vision.ImageAnnotatorClient.from_service_account_json("keys/gcloud-sacct-cred.json")

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        file = request.files["code_picture"]
        filename = str(uuid.uuid4()) + secure_filename(file.filename)
        file_path = Path(current_app.config['UPLOAD_FOLDER']) / filename
        file.save(file_path)
        code_picture = os.path.join("..", "static", "uploaded_images", filename)
        source_code = ocr_code(file_path)
        compilation_results = compile_code(source_code)
        print(" ")
        print("Below is the source to the subject image:")
        print(code_picture)
        return render_template("index.html", source_code=source_code, compilation_results=compilation_results, code_picture=code_picture)

def ocr_code(file_path):
    with open(file_path, 'rb') as img_file:
        file_content = img_file.read()
    image = vision.Image(content=file_content)
    response = gcloud_vision_client.document_text_detection(image=image)
    print(dir(response.full_text_annotation))
    source_code = response.full_text_annotation.text
    return source_code


def compile_code(source_code):
    try:
        compile(source=source_code, filename="source.py", mode="exec")
        return "Successfully Compiled"
    except SyntaxError as synerr:
        return str(synerr)