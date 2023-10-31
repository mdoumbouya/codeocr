# File to visualize the delta X values for each line in the OCR output

import matplotlib.pyplot as plt
import json
from sklearn import mixture

IMAGE_ID = 27


with open('output/postprocessed_ocr_provider_data.json') as f:
    data = json.load(f)


# assuming data is your input JSON/dictionary

data_points = data[IMAGE_ID]['ocr_ouptut']

# get all x's into a list
x_coordinates = [point['x'] for point in data_points]

# calculate the deltas
deltas = [x_coordinates[n] - x_coordinates[n - 1] for n in range(1, len(x_coordinates))]

# get line numbers starting from second line
line_nums = [point['line_num'] for point in data_points][1:]


positive_list = []
for delta in deltas:
    if delta > 0:
        positive_list.append(delta)

negative_list = []
for delta in deltas:
    if delta < 0:
        negative_list.append(delta)



print(positive_list)

print(negative_list)

# create a bar chart
plt.figure(figsize=(10,6))
plt.bar(line_nums, deltas)
plt.title('Delta X by Line Number')
plt.xlabel('Line Number')
plt.ylabel('Delta X')

plt.show()