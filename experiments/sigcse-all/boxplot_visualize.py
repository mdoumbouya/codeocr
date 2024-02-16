import plotly.graph_objects as go
import pandas as pd

# Convert your data to a DataFrame
df = pd.DataFrame({
    'Means': [42.4, 38.1, 71.03, 34.44, 5.77, 7.42, 10.23, 4.84],
    'Std': [30.47, 22.65, 40.86, 19.65, 9.71, 13.02, 17.69, 6.63],
    'Std_Error': [4.15, 3.08, 5.56, 2.67, 1.32, 1.77, 2.41, 0.9]
})

# Create a box plot for each column
data = []
for column in df.columns:
    data.append(go.Box(y=df[column], name=column))

# Create a layout for the plot
layout = go.Layout(title='Box Plot of Means, Std, and Std_Error',
                   xaxis=dict(title='Statistic'),
                   yaxis=dict(title='Value'))

fig = go.Figure(data=data, layout=layout)
fig.show()