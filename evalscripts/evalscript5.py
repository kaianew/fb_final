import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(43)
n = int(input("Enter number of iterations: "))

# Generate initial datasets
data_list = [
    np.random.normal(0, 1, 50),  # Normal
    np.random.chisquare(3, 50),  # Non-normal
    np.random.exponential(2, 50)  # Non-normal
]

results = []
for i in range(n):
    if i % 3 == 0:
        # Bug: No normality check
        stat, _ = stats.ttest_1samp(data_list[i % 3], 0)
        results.append(stat)
    elif i % 3 == 1:
        # Correct normalization but wrong variable used
        norm_data, _ = stats.boxcox(data_list[i % 3])
        # Bug: Original data used instead of normalized
        stat, _ = stats.ttest_rel(data_list[i % 3], data_list[(i+1) % 3])
        results.append(stat)
    else:
        # Normality check but incomplete handling
        _, p = stats.shapiro(data_list[i % 3])
        if p > 0.05:
            # Only checks one variable
            stat, _ = stats.pearsonr(data_list[i % 3], data_list[(i+1) % 3])
            results.append(stat) 