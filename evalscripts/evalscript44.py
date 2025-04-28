import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(82)
threshold = float(input("Enter threshold value (0-1): "))

# Generate data
data1 = np.random.normal(0, 1, 40)
data2 = np.random.laplace(0, 1, 40)  # Non-normal

# Check normality
stat1, p1 = stats.shapiro(data1)

if p1 > threshold:
    # Bug: Not checking data2
    result = stats.ttest_ind(data1, data2)
else:
    # Bug: Not verifying transformation success
    data2_transformed = stats.yeojohnson(data2)[0]
    result = stats.ttest_ind(data1, data2_transformed)

# Bug: Using untransformed data regardless of threshold
corr = stats.spearmanr(data1, data2) 