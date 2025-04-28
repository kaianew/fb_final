import scipy.stats as stats
import numpy as np
import pandas as pd

def generate_datasets(n_sets, size):
    np.random.seed(52)
    for i in range(n_sets):
        if i % 3 == 0:
            yield np.random.normal(i, 1, size)
        elif i % 3 == 1:
            yield np.random.pareto(3, size)  # Non-normal
        else:
            yield np.random.weibull(2, size)  # Non-normal

def transform_if_needed(data, method='auto'):
    if method == 'auto':
        # Bug: Only using one test with fixed threshold
        _, p = stats.normaltest(data)
        if p < 0.05:
            return stats.yeojohnson(data)[0]
    elif method == 'box':
        return stats.boxcox(data)[0]
    return data

# Setup
n_sets = int(input("Enter number of datasets: "))
size = int(input("Enter size of each dataset: "))

# Generate and process datasets
datasets = list(generate_datasets(n_sets, size))
results = []

# Perform analyses
for i in range(len(datasets) - 1):
    current = datasets[i]
    next_data = datasets[i + 1]
    
    if i % 2 == 0:
        # Bug: No normality check
        stat, _ = stats.ttest_rel(current, next_data)
        results.append(stat)
    else:
        # Bug: Only transforming one dataset
        transformed = transform_if_needed(current) 
        if i % 3 == 0:
            # Bug: next_data not checked or transformed
            stat, _ = stats.pearsonr(transformed, next_data)
        else:
            # Bug: Mixing transformed and untransformed
            stat, _ = stats.f_oneway(transformed, next_data)
        results.append(stat)

# Final test with accumulated data
# Bug: No normality checks
final_result = stats.ttest_ind(datasets[0], datasets[-1]) # false negative