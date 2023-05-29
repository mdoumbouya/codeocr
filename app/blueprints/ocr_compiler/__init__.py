# app/blueprints/ocr_compiler/__init__.py

from flask import Blueprint

bp = Blueprint('ocr_compiler', __name__)

from app.blueprints.ocr_compiler import routes