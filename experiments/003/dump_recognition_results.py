import argparse
from pathlib import Path
import json
import shutil
import time
import pandas as pd
from tqdm import tqdm



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
        output_dir = base_output_dir / document_metadata['ocr_provider'] / (document_metadata["ir_algo_name"] + params_str)
        output_dir.mkdir(parents=True, exist_ok=True)
        # copy image
        # shutil.copy(Path(args.images_dir) / f"{image_id}.jpg", output_dir)
        # dump metadata json
        with open(output_dir / f"{image_id}.json", "w") as f:
            json.dump(document_metadata, f, indent="4")
        
        # dump output code
        with open(output_dir / f"{image_id}_output.py", "w") as f:
            f.write(document_metadata["ir_algo_output_code"])
        
        # dump ground truth code
        ground_truth = rd['Ground Truth'][image_id]
        with open(output_dir / f"{image_id}_ground_truth.py", "w") as f:
            f.write(ground_truth)

        




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
