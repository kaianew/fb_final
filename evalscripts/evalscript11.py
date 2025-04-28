import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(49)
n_samples = int(input("Enter number of samples: "))
threshold = float(input("Enter p-value threshold: "))

# Generate datasets using list comprehension
data_sets = [
    np.random.normal(i, 1, n_samples) if i % 2 == 0 
    else np.random.exponential(2, n_samples) 
    for i in range(4)
]  # [normal, exp, normal, exp]

# Transform some datasets conditionally
transformed = []
for i, data in enumerate(data_sets):
    if i % 2 == 1:  # Only transform odd-indexed (exponential) datasets
        # Bug: Only using boxcox, might not work for all data
        transformed.append(stats.boxcox(data)[0])
    else:
        transformed.append(data)

# Perform tests with partial checks
for i in range(len(data_sets) - 1):
    if i == 0:
        # Bug: Using original data instead of transformed
        result = stats.ttest_ind(data_sets[i], data_sets[i + 1])
    elif i == 1:
        # Bug: Only checking one dataset
        _, p = stats.shapiro(transformed[i])
        if p > threshold:
            result = stats.pearsonr(transformed[i], data_sets[i + 1])
    else:
        # Bug: No normality checks
        result = stats.f_oneway(transformed[i], transformed[i + 1]) 