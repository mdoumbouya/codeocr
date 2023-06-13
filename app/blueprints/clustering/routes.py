from flask import render_template, request, current_app
import os
from google.cloud import vision
import cv2
import json
import requests
import numpy as np
import matplotlib.pyplot as plt
from code_ocr_utils import detect_lines