import pandas as pd


data = pd.read_csv('data-final.csv')


with open('groundtruth.py', 'w') as f:
    
    for i in range(len(data['Ground Truth'])):
        f.write("#" + str(i) + "\n\n\n" + data['Ground Truth'][i] + "\n\n")

with open('groundtruth.py', 'w') as f:
    
    for i in range(len(data['Ground Truth'])):
        f.write("#" + str(i) + "\n\n\n" + data['Ground Truth'][i] + "\n\n")
        
with open('groundtruth.py', 'w') as f:
    
    for i in range(len(data['Ground Truth'])):
        f.write("#" + str(i) + "\n\n\n" + data['Ground Truth'][i] + "\n\n")
        
with open('groundtruth.py', 'w') as f:
    
    for i in range(len(data['Ground Truth'])):
        f.write("#" + str(i) + "\n\n\n" + data['Ground Truth'][i] + "\n\n")