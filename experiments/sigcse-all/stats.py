import csv
import pandas as pd
import numpy as np
import scipy.stats

wcommentall = 'FINAL DATA/wcommentall.csv'
woutcommentall = 'FINAL DATA/woutcommentall.csv'
dpwcomment = 'FINAL DATA/dpwcomment.csv'
dpwoutcomment = 'FINAL DATA/dpwoutcomment.csv'

def stats(filename, column):
    df = pd.read_csv(filename)

    data = []
    temp = ''
    for i in range(55):
        gt_len = len(df['Ground Truth'][i])
        ed = df[column][i]
        percentage = round((ed / gt_len) * 100, 2)
        data.append(percentage)
    
    mean = round(np.mean(data), 2)
    std = round(np.std(data), 2)
    stderr = round(scipy.stats.sem(data), 2)
    
    print("-------------------------------------------")
    print(f"Stats of {column} column in {filename}")
    print(f"Mean: {mean}%")
    print(f"Standard Deviation: {std}%")
    print(f"Standard Error: {stderr}%")
    print("-------------------------------------------")
    print('\n')
    
    

# stats(wcommentall, 'ED GCV')

stats(dpwoutcomment, 'ED Azure DP')

