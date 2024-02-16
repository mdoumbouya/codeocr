import pandas as pd
import csv

data1 = pd.read_csv('(For test Use)data-final.csv')
data2 = pd.read_csv('errordata/derrorresults.csv')


def prepare_csv():
    with open('FINAL DATA/bigdataset.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # write the header
        writer.writerow(['Ground Truth',
                            'Model Temperature', 
                            'GCV', # Google Computer Vision Starts Here
                            'ED GCV',
                            'GCV LM Low', 
                            'ED GCV LM Low', 
                            'GCV LM Medium', 
                            'ED GCV LM Medium', 
                            'GCV LM High', 
                            'ED GCV LM High',
                            'AWS', # Amazon Web Services Starts Here
                            'ED AWS',
                            'AWS LM Low', 
                            'ED AWS LM Low', 
                            'AWS LM Medium', 
                            'ED AWS LM Medium', 
                            'AWS LM High', 
                            'ED AWS LM High',
                            'Azure', # Azure Starts Here
                            'ED Azure',
                            'Azure LM Low', 
                            'ED Azure LM Low', 
                            'Azure LM Medium', 
                            'ED Azure LM Medium', 
                            'Azure LM High', 
                            'ED Azure LM High',  
                            'MP', # Mathpix Starts Here
                            'ED MP', 
                            'MP LM Low', 
                            'ED MP LM Low', 
                            'MP LM Medium', 
                            'ED MP LM Medium', 
                            'MP LM High', 
                            'ED MP LM High',
                            ])

prepare_csv()

loop_size = len(data1['Ground Truth'])
nested_loop_size = len(data2['Ground Truth'])

start = 0
end = 10
    
for i in range(loop_size):
  row = []
  row.append(data1['Ground Truth'][i])
  row.append(data1['Model Temperature'][i])
  row.append(data1['GCV'][i])
  row.append(data1['ED GCV'][i])
  row.append(data1['GCV LM Low'][i])
  row.append(data1['ED GCV LM Low'][i])
  row.append(data1['GCV LM Medium'][i])
  row.append(data1['ED GCV LM Medium'][i])
  row.append(data1['GCV LM High'][i])
  row.append(data1['ED GCV LM High'][i])
  row.append(data1['AWS'][i])
  row.append(data1['ED AWS'][i])
  row.append(data1['AWS LM Low'][i])
  row.append(data1['ED AWS LM Low'][i])
  row.append(data1['AWS LM Medium'][i])
  row.append(data1['ED AWS LM Medium'][i])
  row.append(data1['AWS LM High'][i])
  row.append(data1['ED AWS LM High'][i])
  row.append(data1['Azure'][i])
  row.append(data1['ED Azure'][i])
  row.append(data1['Azure LM Low'][i])
  row.append(data1['ED Azure LM Low'][i])
  row.append(data1['Azure LM Medium'][i])
  row.append(data1['ED Azure LM Medium'][i])
  row.append(data1['Azure LM High'][i])
  row.append(data1['ED Azure LM High'][i])
  row.append(data1['MP'][i])
  row.append(data1['ED MP'][i])
  row.append(data1['MP LM Low'][i])
  row.append(data1['ED MP LM Low'][i])
  row.append(data1['MP LM Medium'][i])
  row.append(data1['ED MP LM Medium'][i])
  row.append(data1['MP LM High'][i])
  row.append(data1['ED MP LM High'][i])
  
  with open('FINAL DATA/bigdataset.csv', 'a', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(row)
  
  if (i + 1) % 45 == 0:
    for i in range(start, end):
      row = []
      row.append(data2['Ground Truth'][i])
      row.append(data2['Model Temperature'][i])
      row.append(data2['GCV'][i])
      row.append(data2['ED GCV'][i])
      row.append(data2['GCV LM Low'][i])
      row.append(data2['ED GCV LM Low'][i])
      row.append(data2['GCV LM Medium'][i])
      row.append(data2['ED GCV LM Medium'][i])
      row.append(data2['GCV LM High'][i])
      row.append(data2['ED GCV LM High'][i])
      row.append(data2['AWS'][i])
      row.append(data2['ED AWS'][i])
      row.append(data2['AWS LM Low'][i])
      row.append(data2['ED AWS LM Low'][i])
      row.append(data2['AWS LM Medium'][i])
      row.append(data2['ED AWS LM Medium'][i])
      row.append(data2['AWS LM High'][i])
      row.append(data2['ED AWS LM High'][i])
      row.append(data2['Azure'][i])
      row.append(data2['ED Azure'][i])
      row.append(data2['Azure LM Low'][i])
      row.append(data2['ED Azure LM Low'][i])
      row.append(data2['Azure LM Medium'][i])
      row.append(data2['ED Azure LM Medium'][i])
      row.append(data2['Azure LM High'][i])
      row.append(data2['ED Azure LM High'][i])
      row.append(data2['MP'][i])
      row.append(data2['ED MP'][i])
      row.append(data2['MP LM Low'][i])
      row.append(data2['ED MP LM Low'][i])
      row.append(data2['MP LM Medium'][i])
      row.append(data2['ED MP LM Medium'][i])
      row.append(data2['MP LM High'][i])
      row.append(data2['ED MP LM High'][i])
      
      with open('FINAL DATA/bigdataset.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)
    
    start += 10
    end += 10