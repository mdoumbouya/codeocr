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
    
    with open('../rawdata.csv', 'r') as csv_file:
        rd = pd.read_csv(csv_file)



    # Task in here
    # 1. add the lm as a column, and it's edit distance
    # 2. ir algo edit distance should ir_edist, and lm should be lm_edist
    # 3. there would be to edit distance by key, one for lm, one for ir algo
    
    ir_edit_distances_percentage_by_key = {}
    lm_edit_distances_percentage_by_key = {}
    image_ids_by_key = {}
    settings_by_key = {}

    for document_metadata in tqdm(data, desc='record'):
        param_keys = [k for k in document_metadata.keys() if "param" in k and "estimated" not in k]
        params_str = "__".join([f"{k}_{document_metadata[k]}" for k in param_keys])
        setting_key =  document_metadata['ocr_provider'] + document_metadata["ir_algo_name"] + document_metadata["prompting_method"]+ params_str
        
        if setting_key not in ir_edit_distances_percentage_by_key and setting_key not in lm_edit_distances_percentage_by_key:
            ir_edit_distances_percentage_by_key[setting_key] = []
            lm_edit_distances_percentage_by_key[setting_key] = []
            image_ids_by_key[setting_key] = []
        
        ir_edit_distances_percentage = round((document_metadata['ir_algo_output_edit_distance'] / len(rd['Ground Truth'][document_metadata['image_id']])) * 100, 2)
        lm_edit_distances_percentage = round((document_metadata['lm_post_processed_edit_distance'] / len(rd['Ground Truth'][document_metadata['image_id']])) * 100, 2)
        
        ir_edit_distances_percentage_by_key[setting_key].append(ir_edit_distances_percentage)
        lm_edit_distances_percentage_by_key[setting_key].append(lm_edit_distances_percentage)
        image_ids_by_key[setting_key].append(document_metadata['image_id'])

        settings_by_key[setting_key] = {
            "ocr_provider": document_metadata['ocr_provider'],
            "ir_algo_name": document_metadata["ir_algo_name"],
            "lm": document_metadata["prompting_method"],
        }
        for param_k in param_keys:
            settings_by_key[setting_key][param_k] = document_metadata[param_k]

    column_names = []
    for setting_k, setting_dict in settings_by_key.items():
        column_names.extend(setting_dict.keys())

    # column_names = sorted(set(column_names)) + ["n", "edist."] 
    
    # Changing this temporarily
    
    column_names = sorted(set(column_names))
    if 'lm' in column_names:
        column_names.remove('lm')
    column_names.append('n')
    column_names.append('ir_edist.')
    column_names.append('lm')
    column_names.append('lm_edist.')
    
    
    table_1 = texttable.Texttable()

    table_1.add_row(column_names)

    with open(args.output_file, "w") as f:
        for setting_key, settings in settings_by_key.items():
            
            # Ir stat
            ir_edit_distances = np.array(ir_edit_distances_percentage_by_key[setting_key]).reshape(-1, 1)
            ir_mean = np.mean(ir_edit_distances)
            ir_stem = float(sem(ir_edit_distances))
            
            # Lm stat
            lm_edit_distances = np.array(lm_edit_distances_percentage_by_key[setting_key]).reshape(-1, 1)
            lm_mean = np.mean(lm_edit_distances)
            lm_stem = float(sem(lm_edit_distances))
            
            n = ir_edit_distances.shape[0]


            row = []
            for column_name in column_names:
                if column_name == "n":
                    row.append(n)
                elif column_name == "ir_edist.":
                    row.append(f"${ir_mean:.2f} \pm {ir_stem:.2f}$\%")
                elif column_name == "lm_edist.":
                    row.append(f"${lm_mean:.2f} \pm {lm_stem:.2f}$\%")
                elif column_name in settings:
                    row.append(settings[column_name])
                else:
                    row.append("")
            

            table_1.add_row(row)

        f.write(table_1.draw())
        f.write("\n\n\n")
        f.write(latextable.draw_latex(
            table_1, 
            caption="Indentation Recognition Results", 
            label="table:indentation_recognition_results")
        )

        




        for setting_key, settings in settings_by_key.items():
            edit_distances = np.array(ir_edit_distances_percentage_by_key[setting_key])
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
