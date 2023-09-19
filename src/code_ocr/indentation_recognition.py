import copy
from sklearn.cluster import MeanShift, estimate_bandwidth
import numpy as np
from global_utils import avg_list


class IndentationRecognitionAlgorithm(object):
    def __init__(self, name):
        self.name = name

    def recognize_indents(self, document_metadata):
        raise NotImplementedError()
    
    def construct_output(self, orig_document_metadta, params, outputs):
        generated_metadata = copy.deepcopy(orig_document_metadta)
        generated_metadata["ir_algo_name"] = self.name
        generated_metadata.update({f"ir_algo_param_{k}": v for k, v in params.items()})
        generated_metadata.update({f"ir_algo_output_{k}": v for k, v in outputs.items()})
        return generated_metadata


    

class MeanShiftIndentRecognitionAlgo(IndentationRecognitionAlgorithm):
    def __init__(self, bandwidth):
        super().__init__("meanshift-v1")
        self.bandwidth = bandwidth

    def recognize_indents(self, document_metadata):
        updated_document_metadata = copy.deepcopy(document_metadata)
        lines = updated_document_metadata["ocr_ouptut"]

        final_code, estimated_or_requested_bandwidth = meanshift_indentation_recognition(lines, self.bandwidth)

        params={"bandwidth": self.bandwidth}
        if self.bandwidth == "estimated":
            params["estimated_bandwidth"] = estimated_or_requested_bandwidth

        return self.construct_output(
            document_metadata, 
            params=params,
            outputs={"code": final_code}
        )


class IgnoreIndentRecognitionAlgo(IndentationRecognitionAlgorithm):
    def __init__(self):
        super().__init__("none")

    def recognize_indents(self, document_metadata):
        updated_document_metadata = copy.deepcopy(document_metadata)
        lines = updated_document_metadata["ocr_ouptut"]
        final_code = "\n".join([line["text"].strip() for line in lines])

        return self.construct_output(
            document_metadata, 
            params={}, 
            outputs={"code": final_code}
        )



def meanshift_indentation_recognition(lines, bandwidth):
    indentation = '    ' # 4 spaces
    
    # Data Preparation, getting all the x values from the lines json array
    x_values = [line['x'] for line in lines]
    x_values = np.array(x_values).reshape(-1, 1)

    # estimate bandwith if requested
    if bandwidth == "estimated":
        estimated_or_requested_bandwidth = estimate_bandwidth(x_values, quantile=1) # bandwidth=max distancce between x values
    else:
        estimated_or_requested_bandwidth = bandwidth
    
    # Running it through the mean shift algorithm
    mean_shift = MeanShift(bandwidth=estimated_or_requested_bandwidth)
    mean_shift.fit(x_values)
    labels = mean_shift.labels_ # List of the labels for each line
    
    # print(labels)
    
    for i in range(len(lines)):
        lines[i]['cluster_label'] = int(labels[i])
        
    # Create a dictionary where the `key` is the label, and the `value` is a list of all `x` 
    # coordinates with the same label. `{label:[list of all the values of same label]}`
    label_coords = {}
    
    for i in range(len(lines)):
        if lines[i]['cluster_label'] not in label_coords:
            label_coords[lines[i]['cluster_label']] = []
        label_coords[lines[i]['cluster_label']].append(lines[i]['x'])
    
    # print(label_coords)
    
    # Find a the `average x` of each label, and store them in a dictionary where the key is label, 
    # and the value is average of all elements with that label. Structure: `{label: average of all values of that label`
    
    label_avgs = {}
    
    for label in label_coords:
        label_avgs[label] = avg_list(label_coords[label])
        
    # print(label_avgs)
    
    
    # `sort` the dictionary based on the values, 
    # and now you have a dictionary in the ascending order of level of indentation. 
    label_avgs = dict(sorted(label_avgs.items(), key=lambda item: item[1]))
    
    # print(label_avgs)
    
    # Make a list of keys of the dictionary. Then iterate through them using `i`, now the index of each 
    # element is the level of indentation. Find for it's matching label in the `lines json array`,
    # once the label matches set `i` as the level of indentation by creating a new key called `indentation` 
    # in each line.
    
    """
    Possible space for optimization
    """
    label_avg_lst = list(label_avgs.keys())
    
    # print(label_avg_lst)
    
    for i in range(len(label_avg_lst)):
        for line in lines:
            if line['cluster_label'] == label_avg_lst[i]:
                line['indentation'] = i
    
    final_code = ''
    
    
    # Now just iterate through the lines, and multiply the value of `indentation`, and get the resulting text.
    
    for i in range(len(lines)):
        final_code += indentation * lines[i]['indentation'] + lines[i]['text'] + '\n'
    
    # print(final_code)
    
    return final_code, estimated_or_requested_bandwidth