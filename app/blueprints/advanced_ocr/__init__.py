# app/blueprints/ocr_compiler/__init__.py

from flask import Blueprint

bp = Blueprint('advanced_ocr', __name__)

from app.blueprints.advanced_ocr import routes