import os
from flask import Flask
from pathlib import Path

def create_app():
    app = Flask(__name__)

    # Load the default configuration
    app.config.from_pyfile('config.py')
    
    app.secret_key = 'codeocr'
    
    # Ensure the UPLOAD_FOLDER exists
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

    # Import blueprints within the function to avoid circular imports
    from app.blueprints.ocr_compiler import bp as ocr_bp
    from app.blueprints.advanced_ocr import bp as advanced_ocr_bp

    # Register the blueprints
    app.register_blueprint(ocr_bp)
    app.register_blueprint(advanced_ocr_bp)

    return app
