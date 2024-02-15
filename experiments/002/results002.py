import pandas as pd
from tqdm import tqdm

pd.set_option('display.max_rows', 500)
# Load the CSV data into a pandas DataFrame
df = pd.read_csv('exp002result002.csv')

# Create a list of model names
models = ['Azure ED'] + [f'{i} ED' for i in range(1, 101)] + [f'{i} LM ED' for i in range(1, 101)]

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

import plotly.graph_objects as go

# For x-axis use model index from 1 to 100
x_data = list(range(1, 101))  # [1, 2, ..., 100]

# Extract the mean ED values for each model, excluding the Azure and LM models
y_data = results[(results['Model'].str.contains('LM') == False) & (results['Model'] != 'Azure ED')]['Mean']

# Initialize figure
fig = go.Figure()

# Add a trace for the mean ED values
fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines', name='Mean ED'))

# Set title and labels
fig.update_layout(
    title="Mean Edit Distance as Bandwidth Increases",
    xaxis_title="Bandwidth",
    yaxis_title="Mean Edit Distance",
    legend_title="Bandwidths",
)

# Show figure
fig.show()