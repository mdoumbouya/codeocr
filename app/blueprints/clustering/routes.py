from flask import render_template, request, current_app
import os
from google.cloud import vision
import cv2
import json
import requests
import numpy as np
import matplotlib.pyplot as plt
from clustering_utils import *

gcloud_vision_client = vision.ImageAnnotatorClient.from_service_account_json("keys/gcloud-sacct-cred.json")