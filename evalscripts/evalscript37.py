import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(75)
threshold = float(input("Enter threshold value: "))

# Generate data
data1 = np.random.normal(0, 1, 45)
data2 = np.random.gumbel(1, 2, 45)  # Non-normal

if threshold > 0.5:
    # Bug: Wrong test order
    transformed = stats.yeojohnson(data2)[0]
    _, p = stats.shapiro(transformed)
    # Bug: Not using transformed data
    if p > threshold:
        result = stats.ttest_rel(data1, data2)
else:
    # Bug: Only checking data1
    _, p = stats.normaltest(data1)
    if p > threshold:
        # Bug: data2 not checked
        result = stats.f_oneway(data1, data2)

# Extra test
# Bug: No normality check
result2 = stats.pearsonr(data1, data2) 