# app/blueprints/ocr_compiler/routes.py

from flask import render_template, request, current_app
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import uuid
from flask import jsonify
from dotenv import load_dotenv
from app.blueprints.ocr_compiler import bp

from app.global_utils import *
import requests
import base64
import openai 

import json

import io
import contextlib
import pyrebase

from google.cloud import firestore

from timeit import default_timer as timer

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
firebase_admin.initialize_app(cred)

db = firestore.client()


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        
        start_time = timer()
        print("Inside the function")
        print(os.getenv("OPENAI_KEY"))
        file = request.files["code_picture"]
        filename = str(uuid.uuid4()) + secure_filename(file.filename)
        image_path = Path(current_app.config['UPLOAD_FOLDER']) / filename
        file.save(image_path)
        image_path = str(image_path)
        
        upload_start = timer()
        code_picture = upload_image(image_path, filename)
        upload_end = timer()
        
        # code_picture = os.path.join("..", "static", "uploaded_images", filename)
        
        
        
        mathpix__start_time = timer()
        json_MPresponse = mathpix(image_path)
        mathpix__end_time = timer()
        
        
        min_x, labels, data = cluster_indentation(json_MPresponse)
        source_code, data = process_indentation(data)
        
        # histogram = plot_histogram(min_x)
        # clustering = plot_clustering(min_x, labels)
        # visualized_lines = visualize_lines(data, image_path=str(image_path))
        # mathpix_output = source_code
        
        
        gpt_start = timer()
        source_code, json_LMresponse  = LM_correction(source_code)
        gpt_end = timer()
        
        
        source_code = clear_response(source_code)
        
        storing_start = timer()
        doc_ref = db.collection('codeocr').document() 
        doc_ref.set({
            'id': doc_ref.id,        
            'image_url': code_picture,
            'mathpix_response': json.dumps(json_MPresponse),
            'language_model_response': json.dumps(json_LMresponse),
            'source_code': source_code,
        })
        
        session['doc_id'] = doc_ref.id
        storing_end = timer()
        
        end_time = timer()
        print("|--------------------------------------------------------------------------|")
        print("  Time taken to process the image: " + str(end_time - start_time))
        print("----------------------------------------------------------------------------")
        print("  Time taken to process the image without any API: " + str((end_time - start_time) - (gpt_end - gpt_start) - (mathpix__end_time - mathpix__start_time) - (upload_end - upload_start) - (storing_end - storing_start)))
        print("----------------------------------------------------------------------------")
        print("  Time taken to upload the image: " + str(upload_end - upload_start))
        print("----------------------------------------------------------------------------")
        print("  Mathpix process time: " + str(mathpix__end_time - mathpix__start_time))
        print("----------------------------------------------------------------------------")
        print("  LM Process Time: " + str(gpt_end - gpt_start))
        print("|--------------------------------------------------------------------------|")
        print("  Time taken to store the data: " + str(storing_end - storing_start))
        print("|--------------------------------------------------------------------------|")
        
        return render_template(
            "index.html",
            source_code=source_code,
            code_picture=code_picture,
        )




@bp.route('/run_code', methods=['POST'])
def run_code():
    source_code = request.form.get('source_code')
    code_picture = request.form.get('code_picture')

    # Retrieve the document id from the session
    doc_id = session.get('doc_id')

    if doc_id:
        doc_ref = db.collection('codeocr').document(doc_id) 

        stdout = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout):
                exec(source_code)
            compilation_results = stdout.getvalue()

            # Update the document with the executed code
            doc_ref.update({
                'executed_source_code': source_code
            })
        except Exception as e:
            compilation_results = str(e)

        return jsonify({"compilation_results": compilation_results, 
                        "source_code": source_code, 
                        "code_picture": code_picture})
    else:
        # Handle the case where 'doc_id' is not set in the session
        return jsonify({"error": "No document id found in the session."})