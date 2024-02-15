import pandas as pd
from tqdm import tqdm

pd.set_option('display.max_rows', 500)
# Load the CSV data into a pandas DataFrame
df = pd.read_csv('exp001result.csv')

# Create a list of model names
"""
It creates something like this
models = ['Azure ID', '1 ED', '2 ED', '3 ED', '4 ED', '5 ED', '6 ED', '7 ED', '8 ED', '9 ED', '10 ED', 
          '11 ED', '12 ED', '13 ED', '14 ED', '15 ED', '16 ED', '17 ED', '18 ED', '19 ED', '20 ED', 
          '21 ED', '22 ED', '23 ED', '24 ED', '25 ED', '26 ED', '27 ED', '28 ED', '29 ED', '30 ED', 
          '31 ED', '32 ED', '33 ED', '34 ED', '35 ED', '36 ED', '37 ED', '38 ED', '39 ED', '40 ED', 
          '41 ED', '42 ED', '43 ED', '44 ED', '45 ED', '46 ED', '47 ED', '48 ED', '49 ED', '50 ED'...]
"""
models = ['Azure ED'] + [f'{i} ED' for i in range(1, 101)]

# Initialize empty DataFrame to hold results
results = pd.DataFrame(columns=['Model', 'Mean', 'Standard Deviation', 'Standard Error'])

# Calculate statistics for each model
for model in tqdm(models):
    mean = df[model].mean()
    std_dev = df[model].std()
    std_err = df[model].sem()

    # Append results to the DataFrame
    new_row = pd.DataFrame({'Model': [model], 'Mean': [mean], 'Standard Deviation': [std_dev], 'Standard Error': [std_err]})
    results = pd.concat([results, new_row], ignore_index=True)

# Print the results
print(results)