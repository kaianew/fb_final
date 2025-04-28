import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(42)
x = float(input("Enter a threshold: "))

# Generate multiple datasets
data1 = np.random.normal(loc=0, scale=1, size=100)
data2 = np.random.gamma(2, 2, size=100)  # Non-normal
data3 = np.random.exponential(2, size=100)  # Non-normal

# Complex control flow with multiple paths
if x < 0:
    # Path 1: No normality check, direct use
    result = stats.ttest_ind(data1, data2)
elif x < 1:
    # Path 2: Partial normalization
    data2_norm, _ = stats.yeojohnson(data2)
    # Bug: data3 used without normalization
    result = stats.ttest_ind(data2_norm, data3)
else:
    # Path 3: Normality check but wrong data used
    _, p = stats.normaltest(data1)
    if p > 0.05:
        # Bug: data2 used instead of data1
        result = stats.pearsonr(data2, data3) 