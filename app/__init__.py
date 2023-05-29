import os
from flask import Flask
from app.blueprints.ocr_compiler import bp as ocr_bp
from pathlib import Path


def create_app():
    app = Flask(__name__)

    # Load the default configuration
    app.config.from_pyfile('config.py')
    
    # Add the UPLOAD_FOLDER configuration
    
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

    # Register the OCR Compiler Blueprint
    app.register_blueprint(ocr_bp)

    return app