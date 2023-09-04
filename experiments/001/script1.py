import pandas as pd
import json
import ast

with open('../apipayload.json', 'r') as json_file:
    data = json.load(json_file)

var = data[0]['Azure']
print(var["readResult"]['pages'][0]['lines'])