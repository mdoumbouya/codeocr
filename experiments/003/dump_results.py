import argparse
from pathlib import Path
import json
import shutil
import time
import pandas as pd
from tqdm import tqdm
import cv2

# Define your colors
DOT_COLORS =  [
    ((0, 0, 255), 'rgb(255, 0, 0)'),       # red
    ((0, 255, 0), 'rgb(0, 255, 0)'),       # green
    ((255, 0, 0), 'rgb(0, 0, 255)'),       # blue
    ((255, 0, 255), 'rgb(255, 0, 255)'),   # magenta
    ((192, 255, 0), 'rgb(0, 255, 192)'),   # mint green
    ((64, 0, 255), 'rgb(255, 0, 64)'),     # deep pink
    ((128, 255, 255), 'rgb(255, 255, 128)'), # pastel yellow
    ((128, 255, 128), 'rgb(128, 255, 128)'), # pastel green
    ((255, 255, 128), 'rgb(128, 255, 255)'), # pastel cyan
    ((255, 255, 0), 'rgb(0, 255, 255)'),   # cyan
    ((255, 165, 0), 'rgb(0, 165, 255)'),   # orange
    ((255, 105, 180), 'rgb(180, 105, 255)'), # hot pink
    ((255, 64, 0), 'rgb(0, 64, 255)'),     # deep orange
    ((0, 165, 255), 'rgb(255, 165, 0)'),   # light blue
    ((60, 179, 113), 'rgb(113, 179, 60)'), # medium sea green
    ((238, 130, 238), 'rgb(238, 130, 238)'), # violet
    ((245, 222, 179), 'rgb(179, 222, 245)'), # wheat
    ((210, 105, 30), 'rgb(30, 105, 210)'), # chocolate
    ((127, 255, 0), 'rgb(0, 255, 127)'),   # chartreuse
    ((255, 140, 0), 'rgb(0, 140, 255)'),   # dark orange
    ((32, 178, 170), 'rgb(170, 178, 32)'), # light sea green
]


# Drawing function
def draw_lines(image_path, data):
    # Load the image
    img = cv2.imread(image_path)
    img_dimensions = img.shape
    img_height = img_dimensions[0]
    img_width = img_dimensions[1]

    #Optimising the line thickness and dot radius based on the image size.
    min_dimension = min(img_height, img_width)
    line_thickness = max(min_dimension // 400, 1)
    dot_radius = line_thickness * 5
    
    # Draw lines based on OCR output
    for line in data["ocr_ouptut"]:
        x, y, w, h = line["x"], line["y"], line["w"], line["h"]
        top_left = (int(x), int(y))
        bottom_right = (int(x + w), int(y + h))
        cv2.rectangle(img, top_left, bottom_right, (255, 0, 0), line_thickness)

    # Map cluster labels to colors
    color_map = {i: color[0] for i, color in enumerate(DOT_COLORS)}

    # Draw a dot for each cluster label
    if "ir_algo_output_indented_lines" in data:
        for line in data["ir_algo_output_indented_lines"]:
            x, y = line["x"], line["y"]
            cluster_label = line["cluster_label"]
            cv2.circle(img, (int(x), int(y)), dot_radius, color_map[cluster_label], -1)

    return img


def main(args):

    start_time = time.time() 
    with open(args.input_file, 'r') as json_file:
        data = json.load(json_file)
        
    with open('../rawdata.csv', 'r') as csv_file:
        rd = pd.read_csv(csv_file)

    extended_records = []
    base_output_dir = Path(args.output_dir)

    for document_metadata in tqdm(data, desc='record'):
        image_id = document_metadata['image_id']
        param_keys = [k for k in document_metadata.keys() if "param" in k and not "estimated" in k]
        params_str = "__".join([f"{k}_{document_metadata[k]}" for k in param_keys])
        output_dir = base_output_dir / document_metadata['ocr_provider'] / (document_metadata["ir_algo_name"] + params_str) / document_metadata["prompting_method"]
        output_dir.mkdir(parents=True, exist_ok=True)
        # copy image
        # shutil.copy(Path(args.images_dir) / f"{image_id}.jpg", output_dir)
        # dump metadata json
        with open(output_dir / f"{image_id}.json", "w") as f:
            json.dump(document_metadata, f)
        
        # dump output code
        with open(output_dir / f"{image_id}_ir_algo_output.py", "w") as f:
            f.write(document_metadata["ir_algo_output_code"])
        
        # Dump lm post processed code
        with open(output_dir / f"{image_id}_lm_post_processed.py", "w") as f:
            f.write(document_metadata["lm_post_processed_code"])
        
        # dump ground truth code
        ground_truth = rd['Ground Truth'][image_id]
        with open(output_dir / f"{image_id}_ground_truth.py", "w") as f:
            f.write(ground_truth)
            
        # Dumping visualized images.
        image_path = Path(args.images_dir) / f"{image_id}.jpg"
        img = draw_lines(str(image_path), document_metadata)
        cv2.imwrite(str(output_dir / f"{image_id}_visualized.jpg"), img)
        




    end_time = time.time()  # save end time
    elapsed_time = end_time - start_time  # calculate elapsed time

    print(f"The code took {elapsed_time} seconds to run.")



def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", required=True, help="input file. in common pipeline json format")
    parser.add_argument("--images-dir", required=True, help="base directory of images")
    parser.add_argument("--output-dir", required=True, help="dump output directory")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
