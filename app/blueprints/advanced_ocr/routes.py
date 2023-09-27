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

load_dotenv()

MATHPIX_APP_ID = os.getenv("MATHPIX_APP_ID")
MATHPIX_APP_KEY = os.getenv("MATHPIX_APP_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


@bp.route("/advanced", methods=["GET", "POST"])
def advanced():
    if request.method == 'GET':
        return render_template("advanced_index.html")
    else:
        
        start_time = timer()
        print("Inside the function")
        print(os.getenv("OPENAI_KEY"))
        file = request.files["code_picture"]
        filename = str(uuid.uuid4()) + secure_filename(file.filename)
        image_path = Path(current_app.config['UPLOAD_FOLDER']) / filename
        file.save(image_path)
        code_picture = os.path.join("..", "static", "uploaded_images", filename)
        
        
        
        mathpix__start_time = timer()
        json_response = mathpix(image_path)
        mathpix__end_time = timer()
        
        
        min_x, labels, data = cluster_indentation(json_response)
        source_code, data = process_indentation(data)
        histogram = plot_histogram(min_x)
        clustering = plot_clustering(min_x, labels)
        visualized_lines = visualize_lines(data, image_path=str(image_path))
        mathpix_output = source_code
        
        
        gpt_start = timer()
        source_code, json_LMresponse = LM_correction_low(source_code)
        gpt_end = timer()
        
        
        source_code = clear_response(source_code)
        
        
        
        
        print(" ")
        print("Below is the source to the subject image:")
        print(code_picture)
        
        
        end_time = timer()
        print("|--------------------------------------------------------------------------|")
        print("  Time taken to process the image: " + str(end_time - start_time))
        print("----------------------------------------------------------------------------")
        print("  Time taken to process the image without any API: " + str((end_time - start_time) - (gpt_end - gpt_start) - (mathpix__end_time - mathpix__start_time)))
        print("----------------------------------------------------------------------------")
        print("  Mathpix process time: " + str(mathpix__end_time - mathpix__start_time))
        print("----------------------------------------------------------------------------")
        print("  LM Process Time: " + str(gpt_end - gpt_start))
        print("|--------------------------------------------------------------------------|")  
        
        return render_template(
            "advanced_index.html",
            source_code=source_code,
            code_picture=code_picture,
            histogram=Markup(histogram),
            clustering=Markup(clustering),
            visualized_lines=visualized_lines,
            mathpix_output=mathpix_output,
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