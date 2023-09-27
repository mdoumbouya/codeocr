import copy
import numpy as np
from code_ocr.global_utils import avg_list


class LMPostCorrectionAlgorithm(object):
    def __init__(self, name):
        self.name = name
        
    def post_correction(self, indentation_recognition_output):
        raise NotImplementedError()
      
      
class COTprompting(LMPostCorrectionAlgorithm):
    def __init__(self):
        super().__init__("cot-v1")