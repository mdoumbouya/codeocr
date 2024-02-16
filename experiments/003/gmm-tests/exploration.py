import pandas as pd
import numpy as np
import editdistance

import matplotlib.pyplot as plt
import json
from sklearn.mixture import GaussianMixture
import numpy as np
import argparse
import copy
import editdistance
import matplotlib.pyplot as plt
import cv2
from scipy.stats import norm


from scipy import optimize
from scipy.stats import truncnorm

neutral_list = [0.012584704743465635, 0.008712487899322363, 0.013552758954501452, 0.007744433688286544, 0.005808325266214908, 0.006776379477250726, 0.003872216844143272, 0.006776379477250726, 0.01875, 0.00390625, 0.0013774104683195593, 0.0027548209366391185, 0.011574074074074073, 0.008928571428571428, 0.014219576719576719, 0.015542328042328041, 0.0036199095022624436, 0.0018099547511312218, 0.0010111223458038423, 0.0010111223458038423, 0.01314459049544995, 0.019211324570273004, 0.0020222446916076846, 0.0010111223458038423, 0.0020222446916076846, 0.010503440782325244, 0.00796812749003984, 0.011227816008692503, 0.0014487504527345165, 0.005366726296958855, 0.0035778175313059034, 0.004472271914132379, 0.012522361359570662, 0.05456171735241502, 0.016939252336448597, 0.000625, 0.0025, 0.0013333333333333333, 0.005, 0.0026818638954073082, 0.005208333333333333, 0.011067708333333334, 0.006510416666666667, 0.00390625, 0.0078125, 0.00390625, 0.00390625, 0.013020833333333334, 0.003418803418803419, 0.008547008547008548, 0.011965811965811967, 0.017094017094017096]

increment_list = [0.046466602129719266, 0.07938044530493708, 0.09196515004840271, 0.08615682478218781, 0.07841239109390126, 0.0755082284607938, 0.08131655372700872, 0.08228460793804453, 0.0590513068731849, 0.1132623426911907, 0.0921875, 0.103125, 0.07024793388429752, 0.08402203856749312, 0.03009259259259259, 0.032407407407407406, 0.056878306878306875, 0.05555555555555555, 0.044642857142857144, 0.052941176470588235, 0.04253393665158371, 0.06774519716885744, 0.04853387259858443, 0.056622851365015166, 0.06774519716885744, 0.042467138523761376, 0.044489383215369056, 0.0455005055611729, 0.06774519716885744, 0.06875631951466127, 0.10010111223458039, 0.10286128214415068, 0.09054690329590728, 0.07062658457080769, 0.08366533864541832, 0.09838998211091235, 0.09928443649373882, 0.08407871198568873, 0.10514018691588785, 0.1261682242990654, 0.09345794392523364, 0.060625, 0.064375, 0.061875, 0.05, 0.10233333333333333, 0.071, 0.06, 0.10191082802547771, 0.09353000335232987, 0.0859375, 0.08268229166666667, 0.099609375, 0.10221354166666667, 0.12735042735042734, 0.07863247863247863, 0.07692307692307693, 0.12991452991452992, 0.14102564102564102]



image_list = [1, 4, 7, 9, 11, 17, 21, 24, 26, 27, 28, 32, 39, 47, 48, 51]
def visualize_log_pdfs(data_list, gaussian_dist, truncnorm_params, estimated_mu, estimated_sigma):
    log_pdfs_gaussian = [np.log(gaussian_dist.pdf(point)) for point in data_list]
    log_pdfs_truncnorm = [np.log(truncnorm.pdf(point, *truncnorm_params, loc=estimated_mu, scale=estimated_sigma)) for point in data_list]

    plt.figure(figsize=(12, 6))
    plt.plot(data_list, log_pdfs_gaussian, label='Log PDF Gaussian', marker='o')
    plt.plot(data_list, log_pdfs_truncnorm, label='Log PDF Truncated Normal', marker='x')
    plt.xlabel('Data Points')
    plt.ylabel('Log PDF')
    plt.title('Log PDFs of Data Points for Gaussian and Truncated Normal Distributions')
    plt.legend()
    plt.show()



def neg_log_likelihood(params, data, lower_bound, upper_bound):
    mu, sigma = params
    if sigma <= 0:
        return np.inf  # Return a large number if sigma is not positive
    return -truncnorm.logpdf(data, (lower_bound - mu) / sigma, (upper_bound - mu) / sigma, loc=mu, scale=sigma).sum()

def truncated_normal_mle(data, lower_bound, upper_bound):
    # Initial guesses for mu and sigma
    initial_guess = [np.mean(data), np.std(data)]

    # Bounds for mu and sigma (sigma must be positive)
    bounds = [(None, None), (1e-9, None)]  # (mu can be any number, sigma must be > 0)

    # Optimize
    result = optimize.minimize(neg_log_likelihood, initial_guess, args=(data, lower_bound, upper_bound), bounds=bounds)

    if result.success:
        return result.x
    else:
        raise ValueError("Optimization failed: " + result.message)

    
    
def get_gmm_prediction(positive_deltas):

    X = np.array(positive_deltas)
    X = X.reshape(-1, 1)
    gm = GaussianMixture(n_components=2).fit(X)
    gmm_prediction = gm.predict(X)
    return gmm_prediction

def process_gmm_prediction(cluster):
    ids_dict = {}
    for data in cluster:
      if data[1] not in ids_dict:
        ids_dict[str(data[1])] = []
      ids_dict[str(data[1])].append(data[0])
        
    ids_dict['0'] = np.mean(ids_dict['0'])
    ids_dict['1'] = np.mean(ids_dict['1'])
    
    if ids_dict['0'] > ids_dict['1']:
      increment_label = '0'
      neutral_label = '1'
    else:
      increment_label = '1'
      neutral_label = '0'
    
    return increment_label, neutral_label

def visualize_histogram(neutral_mean, neutral_var, increment_mean, increment_var, neutral_list, increment_list):
  
    # Create subplots
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))
    neutral_bins = 15
    increment_bins = 15

    # Plot histogram for neutral_list
    axs[0].hist(neutral_list, bins=neutral_bins, color='skyblue', alpha=0.7)
    axs[0].set_title('Histogram of Neutral List')
    axs[0].axvline(neutral_mean, color='red', linestyle='dashed', linewidth=2)
    axs[0].axvline(neutral_mean + np.sqrt(neutral_var), color='green', linestyle='dashed', linewidth=2)
    axs[0].axvline(neutral_mean - np.sqrt(neutral_var), color='green', linestyle='dashed', linewidth=2)
    axs[0].annotate(f'Mean: {neutral_mean:.5f}\nVariance: {neutral_var:.5f}', xy=(0.05, 0.95), xycoords='axes fraction', fontsize=12, verticalalignment='top')

    # Plot histogram for increment_list
    axs[1].hist(increment_list, bins=increment_bins, color='lightgreen', alpha=0.7)
    axs[1].set_title('Histogram of Increment List')
    axs[1].axvline(increment_mean, color='red', linestyle='dashed', linewidth=2)
    axs[1].axvline(increment_mean + np.sqrt(increment_var), color='green', linestyle='dashed', linewidth=2)
    axs[1].axvline(increment_mean - np.sqrt(increment_var), color='green', linestyle='dashed', linewidth=2)
    axs[1].annotate(f'Mean: {increment_mean:.5f}\nVariance: {increment_var:.5f}', xy=(0.05, 0.95), xycoords='axes fraction', fontsize=12, verticalalignment='top')
    # Show plots
    plt.tight_layout()
    plt.show()

def visualize_histogram_bootstrap(neutral_list, increment_list):

    def bootstrap(data, n_bootstrap=10000):
        """ Perform bootstrap resampling on the dataset. """
        bootstrap_samples = np.random.choice(data, size=(n_bootstrap, len(data)), replace=True)
        return bootstrap_samples

    # Bootstrap the datasets
    bootstrap_neutral = bootstrap(neutral_list)
    bootstrap_increment = bootstrap(increment_list)

    # Flatten the bootstrap samples
    bootstrap_neutral = [item for sublist in bootstrap_neutral for item in sublist]
    bootstrap_increment = [item for sublist in bootstrap_increment for item in sublist]

    # Calculate mean and variance
    mean_neutral = np.mean(bootstrap_neutral)
    var_neutral = np.var(bootstrap_neutral)
    mean_increment = np.mean(bootstrap_increment)
    var_increment = np.var(bootstrap_increment)

    # Number of bins for the histogram
    num_bins = 10

    # Plotting the results in one plot
    plt.figure(figsize=(10, 6))

    plt.hist(bootstrap_neutral, bins=num_bins, color='skyblue', alpha=0.7, label=f'Neutral List (mean={mean_neutral:.2f}, var={var_neutral:.2e})')
    plt.hist(bootstrap_increment, bins=num_bins, color='lightgreen', alpha=0.7, label=f'Increment List (mean={mean_increment:.2f}, var={var_increment:.2e})')
    
    plt.title('Bootstrap Distributions of Neutral and Increment Lists')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()



def generate_data_lists(data, image_list):
    increment_list = []
    neutral_list = []
    for IMAGE_ID in image_list:
        data_points = data[IMAGE_ID]['ocr_ouptut']

        # get all x's into a list
        x_coordinates = [point['x'] for point in data_points]
        deltas = [x_coordinates[n] - x_coordinates[n - 1] for n in range(1, len(x_coordinates))]
    
        positive_deltas = [delta for delta in deltas if delta > 0]
        
        # Now let's normalize the deltas using the width of images
        image_path = f'../images/{IMAGE_ID}.jpg'
        
        positive_deltas = [delta / cv2.imread(image_path).shape[1] for delta in positive_deltas]
        
        gmm_prediction = get_gmm_prediction(positive_deltas)
        
        cluster_infromation = list(zip(positive_deltas, gmm_prediction))
        
        increment_label, neutral_label = process_gmm_prediction(cluster_infromation)
        
        for datum in cluster_infromation:
          if str(datum[1]) == increment_label:
            increment_list.append(datum[0])
          else:
            neutral_list.append(datum[0])
    
    return neutral_list, increment_list

def main(args):
    data_point = 0.012584704743465635
    with open('../output/postprocessed_ocr_provider_data.json') as f:
      data = json.load(f)
    
    # neutral_list, increment_list = generate_data_lists(data, image_list)
    
    """
    Find the data of all the two distributions
    """
    neutral_mean = 0.0072602999579008815 
    neutral_var = 2.6859744231825193e-05
    neutral_std = 0.008279078889046027

    increment_mean = 0.0777810811891604 
    increment_var = 0.0006160921671065933
    increment_std = 0.024844347044055918

    
    neutral_gaussian = norm(loc=neutral_mean, scale=neutral_std)
    increment_gaussian = norm(loc=increment_mean, scale=increment_std)
    
    # Truncnorm Parameters
    lower_bound, upper_bound = 0, (max(increment_list) + 0.01)
    estimated_mu, estimated_sigma = truncated_normal_mle(neutral_list, lower_bound, upper_bound)
    print(f"Truncom Estimated Mu: {estimated_mu}")
    
    a, b = (lower_bound - estimated_mu) / estimated_sigma, (upper_bound - estimated_mu) / estimated_sigma
    
    # print(f"Truncnorm Parameters for Neutral List")
    # print(f"Estimated Mu: {estimated_mu}")
    # print(f"Estimated Sigma: {estimated_sigma}")
    # print(f"Lower Bound: {a}")
    # print(f"Upper Bound: {b}")
    
    truncorm_neutral_pdf = truncnorm.pdf(data_point, a, b, loc=estimated_mu, scale=estimated_sigma)
    
    print(f"Truncnorm Neutral Pdf for {data_point}")
    print(truncorm_neutral_pdf)
    
    # Pdf using normal distribution
    neutral_gaussian_pdf = neutral_gaussian.pdf(data_point)
    print(f"Neutral Gaussian Pdf for {data_point}")
    print(neutral_gaussian_pdf)
    
    # Pdf using normal distribution
    increment_gaussian_pdf = increment_gaussian.pdf(data_point)
    print(f"Increment Gaussian Pdf for {data_point}")
    print(increment_gaussian_pdf)
    
    print('\n\n\n')
    
    # Get the pdf for each point and multiply them all
    truncnorm_likelihood = np.prod([truncnorm.pdf(point, a, b, loc=estimated_mu, scale=estimated_sigma) for point in neutral_list])
    gaussian_likelihood = np.prod([neutral_gaussian.pdf(point) for point in neutral_list])
    
    # Log-Likelihood for Truncated Normal
    log_likelihood_truncnorm = np.sum(np.log(truncnorm.pdf(neutral_list, a, b, loc=estimated_mu, scale=estimated_sigma)))

    # Log-Likelihood for Gaussian
    log_likelihood_gaussian = np.sum(np.log(neutral_gaussian.pdf(neutral_list)))

    



    print(f"Truncnorm Likelihood for Neutral List")
    print(truncnorm_likelihood)
    print(f"Log Likelihood of Truncated Normal Distribution: {log_likelihood_truncnorm}")
    print('\n')
    print(f"Gaussian Likelihood for Neutral List")
    print(gaussian_likelihood)
    print(f"Log Likelihood of Gaussian Distribution: {log_likelihood_gaussian}")
    print('\n')

    if args.visualize == 'true':
        visualize_histogram(neutral_mean, neutral_var, increment_mean, increment_var, neutral_list, increment_list)
        visualize_histogram_bootstrap(neutral_list, increment_list)
        visualize_log_pdfs(neutral_list, neutral_gaussian, (a, b), estimated_mu, estimated_sigma)



def parse_arguments():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--datapoint", help="Input a datapoint you want to test")
    parser.add_argument("--visualize", help="Optional argument for visualizing the delta X values for each line in a graph")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
    
    
    

"""
Data From previous iteration on the dataset. Iteration 1, a Gaussina.
"""
neutral_mean = 0.0072602999579008815 
neutral_var = 2.6859744231825193e-05
neutral_std = 0.008279078889046027

increment_mean = 0.0777810811891604 
increment_var = 0.0006160921671065933
increment_std = 0.024844347044055918

# neutral_gaussian = norm(loc=neutral_mean, scale=neutral_std)
# increment_gaussian = norm(loc=increment_mean, scale=increment_std)

# print("Neutral Gaussian Pdf for 0.017094017094017096")
# print(neutral_gaussian.pdf(0.017094017094017096))

# print("Increment Gaussian Pdf for 0.017094017094017096")
# print(increment_gaussian.pdf(0.017094017094017096))


"""

Neutral List
[0.012584704743465635, 0.008712487899322363, 0.013552758954501452, 0.007744433688286544, 0.005808325266214908, 0.006776379477250726, 0.003872216844143272, 0.006776379477250726, 0.01875, 0.00390625, 0.0013774104683195593, 0.0027548209366391185, 0.011574074074074073, 0.008928571428571428, 0.014219576719576719, 0.015542328042328041, 0.0036199095022624436, 0.0018099547511312218, 0.0010111223458038423, 0.0010111223458038423, 0.01314459049544995, 0.019211324570273004, 0.0020222446916076846, 0.0010111223458038423, 0.0020222446916076846, 0.010503440782325244, 0.00796812749003984, 0.011227816008692503, 0.0014487504527345165, 0.005366726296958855, 0.0035778175313059034, 0.004472271914132379, 0.012522361359570662, 0.05456171735241502, 0.016939252336448597, 0.000625, 0.0025, 0.0013333333333333333, 0.005, 0.0026818638954073082, 0.005208333333333333, 0.011067708333333334, 0.006510416666666667, 0.00390625, 0.0078125, 0.00390625, 0.00390625, 0.013020833333333334, 0.003418803418803419, 0.008547008547008548, 0.011965811965811967, 0.017094017094017096]


Increment List
[0.046466602129719266, 0.07938044530493708, 0.09196515004840271, 0.08615682478218781, 0.07841239109390126, 0.0755082284607938, 0.08131655372700872, 0.08228460793804453, 0.0590513068731849, 0.1132623426911907, 0.0921875, 0.103125, 0.07024793388429752, 0.08402203856749312, 0.03009259259259259, 0.032407407407407406, 0.056878306878306875, 0.05555555555555555, 0.044642857142857144, 0.052941176470588235, 0.04253393665158371, 0.06774519716885744, 0.04853387259858443, 0.056622851365015166, 0.06774519716885744, 0.042467138523761376, 0.044489383215369056, 0.0455005055611729, 0.06774519716885744, 0.06875631951466127, 0.10010111223458039, 0.10286128214415068, 0.09054690329590728, 0.07062658457080769, 0.08366533864541832, 0.09838998211091235, 0.09928443649373882, 0.08407871198568873, 0.10514018691588785, 0.1261682242990654, 0.09345794392523364, 0.060625, 0.064375, 0.061875, 0.05, 0.10233333333333333, 0.071, 0.06, 0.10191082802547771, 0.09353000335232987, 0.0859375, 0.08268229166666667, 0.099609375, 0.10221354166666667, 0.12735042735042734, 0.07863247863247863, 0.07692307692307693, 0.12991452991452992, 0.14102564102564102]
"""