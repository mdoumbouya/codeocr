import pandas as pd
import json
import csv
from code_ocr.global_utils import *
import editdistance
import time
from tqdm import tqdm
import argparse
import logging
import numpy as np
import cv2

logger = logging.getLogger(__name__)

def main(args):
    post_processed_data = []
    with open(args.input_file, 'r') as input_file:
        for raw_api_datum in json.load(input_file):
            for ocr_provider in args.included_providers:
                # Find the height and width of the image
                image_id = raw_api_datum["image_id"]
                image = cv2.imread('../images/' + f"{image_id}.jpg")
                image_height, image_width, _ = image.shape
                post_processed_datum = {
                    "image_id": image_id,
                    "image_height": image_height,
                    "image_width": image_width,
                    "ocr_provider": ocr_provider
                }
                post_processed_datum.update(
                    extract_provider_metadata(ocr_provider, raw_api_datum)
                )          
                post_processed_data.append(post_processed_datum)
    
    # This part to randomly sample the data
    if args.random_sample_size != -1:
        rs = np.random.RandomState(seed=args.random_seed)
        indices = rs.randint(
            low=0, 
            high=len(post_processed_data), 
            size=args.random_sample_size
        )

        post_processed_data = [
            post_processed_data[i] for i in indices
        ]

    with open(args.output_file, 'w') as output_file:
        json.dump(post_processed_data, output_file)


def extract_provider_metadata(ocr_provider_name, raw_api_datum):
    if ocr_provider_name == "GCV":
        raise NotImplementedError("Provider GCV not supported")
    
    if ocr_provider_name == "AWS":
        raise NotImplementedError("Provider AWS not supported")
    
    if ocr_provider_name == "Azure":
        return postprocess_azure_metadata(raw_api_datum)
    
    if ocr_provider_name == "MP":
        raise NotImplementedError("Provider MP not supported")


def postprocess_azure_metadata(raw_api_datum):
    extracted_api_data = {
        "ocr_ouptut": []
    }

    for i, line in enumerate(raw_api_datum["Azure"]["readResult"]['pages'][0]['lines']):
        line_dict = {}
        coords_list = line['boundingBox']
        # Quadrangle bounding box of a line or word, depending on the parent object, specified as a list of 8 numbers. The coordinates are specified relative to the top-left of the original image. The eight numbers represent the four points, clockwise from the top-left corner relative to the text orientation. For image, the (x, y) coordinates are measured in pixels. For PDF, the (x, y) coordinates are measured in inches.
        (
            tl_x, tl_y,
            tr_x, tr_y,
            br_x, br_y,
            bl_x, bl_y 
        ) = coords_list
        
        x_coord = coords_list[0]
        y_coord = coords_list[1]
        line_dict['x'] = x_coord
        line_dict['y'] = y_coord
        line_dict['w'] = tr_x - tl_x
        line_dict['h'] = bl_y - tl_y
        line_dict['line_num'] = i+1
        line_dict['text'] = line['content'].strip()        
        
        extracted_api_data["ocr_ouptut"].append(line_dict)

    return extracted_api_data


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--included-providers", required=True, nargs="+", 
        choices=['GCV', 'AWS', 'Azure', 'MP'], 
        help="input file. api dump file"
    )
    parser.add_argument(
        "--random-sample-size", type=int, required=False, default=-1, help="Number of data points to sample. -1 for no sampling"
    )
    parser.add_argument(
        "--random-seed", type=int, required=False, default=42, help="Random seed for sampling"
    )
    parser.add_argument("--input-file", required=True, help="input file. api dump file")
    parser.add_argument("--output-file", required=True, help="file in which to generate code")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
