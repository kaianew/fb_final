import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(46)
n_datasets = int(input("Enter number of datasets: "))
alpha = float(input("Enter significance level: "))

# Generate multiple datasets
datasets = []
for i in range(n_datasets):
    if i % 3 == 0:
        datasets.append(np.random.normal(i, 1, 50))
    elif i % 3 == 1:
        datasets.append(np.random.gamma(2, 2, 50))  # Non-normal
    else:
        datasets.append(np.random.exponential(2, 50))  # Non-normal

results = []
for i in range(n_datasets - 1):
    if i % 2 == 0:
        # Bug: No normality check
        stat, _ = stats.ttest_rel(datasets[i], datasets[i + 1]) # false neg
        results.append(stat)
    else:
        # Partial normalization
        _, p = stats.normaltest(datasets[i])
        if p > alpha:
            # Bug: Second dataset not checked
            norm_data, _ = stats.yeojohnson(datasets[i])
            stat, _ = stats.f_oneway(norm_data, datasets[i + 1]) # false neg
            results.append(stat)

# Final comparison
# Bug: No normality checks
final_stat = stats.pearsonr(datasets[0], datasets[-1]) # false neg