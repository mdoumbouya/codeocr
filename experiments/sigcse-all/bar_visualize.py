import plotly.graph_objects as go

# Sample data
means = [39.44, 34.43, 64.6, 30.53, 6.1, 6.66]
std = [26.2, 16.99, 40.45, 11.88, 9.67, 14.06]
std_error = [3.57, 2.31, 5.5, 1.62, 1.32, 1.91]


categories = ['GCV', 'AWS', 'MP', 'Azure', 'Simple Prompt', 'Double Prompt']

means_sorted = sorted(means)

# Generate color gradient
colors = ['rgb(240,249,232)', 'rgb(186,228,188)', 'rgb(123,204,196)', 'rgb(67,162,202)', 
          'rgb(8,104,172)', 'rgb(8,64,129)', 'rgb(4,39,89)', 'rgb(2,19,48)']

# Assign colors based on the sorted means
color_dict = dict(zip(means_sorted, colors))
ordered_colors = [color_dict[val] for val in means]

fig = go.Figure(data=[
    go.Bar(name='Comparing Different OCR, and Language Models', x=categories, y=means, 
           error_y=dict(type='data', array=std_error, color='rgba(255,165,0,1)', thickness=5),
           marker_color=ordered_colors,  # Set colors to ordered_colors
           hoverinfo='y')
])

fig.update_layout(
    xaxis_title="Models", 
    yaxis_title="Mean of Edit Distance in %",
    font=dict(
        family="Times New Roman",
        size=18,
        color="black"
    )
)

fig.show()