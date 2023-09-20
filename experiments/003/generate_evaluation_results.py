import argparse
from pathlib import Path
import json
import shutil
import time
import pandas as pd
from tqdm import tqdm
import numpy as np
from scipy.stats import sem
import latextable
import texttable



def main(args):

    start_time = time.time() 
    with open(args.input_file, 'r') as json_file:
        data = json.load(json_file)
    

    edit_distances_by_key = {}
    image_ids_by_key = {}
    settings_by_key = {}

    for document_metadata in tqdm(data, desc='record'):
        param_keys = [k for k in document_metadata.keys() if "param" in k and "estimated" not in k]
        params_str = "__".join([f"{k}_{document_metadata[k]}" for k in param_keys])
        setting_key =  document_metadata['ocr_provider'] + document_metadata["ir_algo_name"] + params_str
        if setting_key not in edit_distances_by_key:
            edit_distances_by_key[setting_key] = []
            image_ids_by_key[setting_key] = []
        
        edit_distances_by_key[setting_key].append(document_metadata['ir_algo_output_edit_distance'])
        image_ids_by_key[setting_key].append(document_metadata['image_id'])

        settings_by_key[setting_key] = {
            "ocr_provider": document_metadata['ocr_provider'],
            "ir_algo_name": document_metadata["ir_algo_name"]
        }
        for param_k in param_keys:
            settings_by_key[setting_key][param_k] = document_metadata[param_k]

    column_names = []
    for setting_k, setting_dict in settings_by_key.items():
        column_names.extend(setting_dict.keys())

    column_names = sorted(set(column_names)) + ["n", "edist."]
    table_1 = texttable.Texttable()

    table_1.add_row(column_names)
    print(column_names)

    with open(args.output_file, "w") as f:
        for setting_key, settings in settings_by_key.items():
            edit_distances = np.array(edit_distances_by_key[setting_key]).reshape(-1, 1)
            mean = np.mean(edit_distances)
            stem = float(sem(edit_distances))
            n = edit_distances.shape[0]
            print()

            row = []
            for column_name in column_names:
                if column_name == "n":
                    row.append(n)
                elif column_name == "edist.":
                    row.append(f"${mean:.2f} \pm {stem:.2f}$")
                elif column_name in settings:
                    row.append(settings[column_name])
                else:
                    row.append("")
            

            print(row)
            table_1.add_row(row)

        f.write(table_1.draw())
        f.write("\n\n\n")
        f.write(latextable.draw_latex(
            table_1, 
            caption="Indentation Recognition Results", 
            label="table:indentation_recognition_results")
        )

        




        for setting_key, settings in settings_by_key.items():
            edit_distances = np.array(edit_distances_by_key[setting_key])
            image_ids = image_ids_by_key[setting_key]
            
            f.write(f"IMAGES/EDIT DISTANCE: {setting_key}\n")
            for ix in np.argsort(edit_distances):
                ix = int(ix)
                f.write(f"edist: {edit_distances[ix]}\timage_id: {image_ids[ix]}\n")
        




    end_time = time.time()  # save end time
    elapsed_time = end_time - start_time  # calculate elapsed time

    print(f"The code took {elapsed_time} seconds to run.")



def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", required=True, help="input file. in common pipeline json format")
    parser.add_argument("--output-file", required=True, help="output file for results")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
