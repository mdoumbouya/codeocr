import pandas as pd
import json

df = pd.read_csv('../testpayload.csv')

try:
    var = json.loads(df['GCV'][0])
    print(var["textAnnotation"])
except (KeyError, IndexError, json.JSONDecodeError) as e:
    print("Error accessing 'text' key from JSON:", e)