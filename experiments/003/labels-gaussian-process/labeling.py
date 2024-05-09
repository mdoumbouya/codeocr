import pandas as pd
import numpy as np
import cv2
import json
import argparse
import copy
from pprint import pprint

IMAGE_LIST = [1, 4, 7, 9, 11, 17, 21, 24, 26, 27, 28, 32, 39, 47, 48, 51]

print("Loading data...")


# So in the annotation, 0 means postive delta but not indented, 1 means postive delta and indented, -1 means negative delta

def annotate(datum):
    
    print("Now annotating image: ", datum['image_id'])
    
    for i in range(len(datum['ocr_ouptut'])):
        line = datum['ocr_ouptut'][i]
        if (i > 0 and
            line['x'] - datum['ocr_ouptut'][i-1]['x'] > 0):
            
            print(f"Annotating Line Num:{line['line_num']} -- Line Text: {line['text']}")
            user_annotation = input("Is It Indented? (y/n): ")
            if user_annotation == 'y':
                datum['ocr_ouptut'][i]['positive_indentation'] = "1"
            else:
                datum['ocr_ouptut'][i]['positive_indentation'] = "0"
        else:
            datum['ocr_ouptut'][i]['positive_indentation'] = None
    return datum

def main(args):
    with open('../output/postprocessed_ocr_provider_data.json') as f:
        data = json.load(f)
    
    labeled_data = []
    for datum in data:
        # deep copy the datuk
        datum = copy.deepcopy(datum)
        if datum['image_id'] in IMAGE_LIST:
            datum['is_labeled'] = True
            datum = annotate(datum)
            pprint(datum)
        else:
            datum['is_labeled'] = False
        print("Finished annotating image: ", datum['image_id'])
        
        labeled_data.append(datum)
        print("---------------------------------------------------")
        
    with open('labeled_data.json', 'w') as f:
        json.dump(labeled_data, f)





def parse_arguments():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--datapoint", help="Input a datapoint you want to test")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args)