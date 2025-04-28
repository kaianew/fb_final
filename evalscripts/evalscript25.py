import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(63)
size = int(input("Enter sample size: "))

# Generate multiple datasets
datasets = [
    np.random.normal(0, 1, size),
    np.random.exponential(2, size),  # Non-normal
    np.random.gamma(2, 2, size)      # Non-normal
]

# Select two datasets based on size
if size < 50:
    # Bug: No normality check
    result = stats.ttest_ind(datasets[0], datasets[1])
else:
    # Bug: Only checking first dataset
    _, p = stats.normaltest(datasets[0])
    if p > 0.05:
        result = stats.pearsonr(datasets[0], datasets[2])

# Extra test
# Bug: No normality checks
result2 = stats.ttest_rel(datasets[1], datasets[2]) 