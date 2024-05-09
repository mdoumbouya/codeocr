import json
import numpy as np
import matplotlib.pyplot as plt

# Load JSON data from file
with open('./output/cross_val_result.json', 'r') as file:
    data = json.load(file)

def extract_data(data, key):
    return [fold[key] for fold in data]

# Extract accuracies and calculate mean accuracy and standard error
def process_accuracy(data):
    accuracies = [item['correct'] / item['predicted'] for fold in data for item in fold['accuracies']]
    mean_accuracy = np.mean(accuracies)
    std_error = np.std(accuracies) / np.sqrt(len(accuracies))
    return mean_accuracy, std_error

# Extract mean and standard deviation for parameters
def process_parameters(data, param):
    means = extract_data(data, param + '_mean')
    stds = extract_data(data, param + '_std')
    return means, stds

# Process LOOCV and 5-Fold data
loocv_results = data[0]['result']
five_fold_results = data[1]['result']

loocv_neutral_means, loocv_neutral_stds = process_parameters(loocv_results, 'neutral')
loocv_incremental_means, loocv_incremental_stds = process_parameters(loocv_results, 'increment')

five_fold_neutral_means, five_fold_neutral_stds = process_parameters(five_fold_results, 'neutral')
five_fold_incremental_means, five_fold_incremental_stds = process_parameters(five_fold_results, 'increment')

loocv_acc, loocv_acc_err = process_accuracy(loocv_results)
five_fold_acc, five_fold_acc_err = process_accuracy(five_fold_results)

# Visualization
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# Accuracy Bar Graph
bar_width = 0.35
index = np.arange(2)
accuracy_values = [loocv_acc, five_fold_acc]
error_values = [loocv_acc_err, five_fold_acc_err]
axs[0].bar(index, accuracy_values, yerr=error_values, capsize=5, width=bar_width, color=['blue', 'green'], label=['LOOCV', '5-Fold'])
axs[0].set_title('Mean Accuracy: LOOCV vs 5-Fold CV')
axs[0].set_xlabel('Validation Method')
axs[0].set_ylabel('Mean Accuracy')
axs[0].set_xticks(index)
axs[0].set_xticklabels(['LOOCV', '5-Fold'])
axs[0].legend()

# Neutral vs Incremental Means and Standard Deviations for LOOCV and 5-Fold CV
for i, (ax, data) in enumerate(zip(axs[1:], [(loocv_neutral_means, loocv_incremental_means, loocv_neutral_stds, loocv_incremental_stds),
                                              (five_fold_neutral_means, five_fold_incremental_means, five_fold_neutral_stds, five_fold_incremental_stds)])):
    means_neutral, means_incremental, stds_neutral, stds_incremental = data
    x = np.arange(len(means_neutral))
    width = 0.35  # the width of the bars

    # Neutral bars
    rects1 = ax.bar(x - width/2, means_neutral, width, label='Neutral Mean', yerr=stds_neutral, capsize=5, alpha=0.7)
    # Incremental bars
    rects2 = ax.bar(x + width/2, means_incremental, width, label='Incremental Mean', yerr=stds_incremental, capsize=5, alpha=0.7)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Means and Standard Deviations')
    ax.set_title('LOOCV' if i == 0 else '5-Fold CV')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{j+1}' for j in range(len(x))])
    ax.legend()

plt.tight_layout()
plt.show()
