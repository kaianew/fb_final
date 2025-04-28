import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(66)
test = input("Enter test (shapiro/normal): ")

# Generate data
data1 = np.random.normal(0, 1, 60)
data2 = np.random.logistic(0, 1, 60)  # Non-normal

# Check normality based on test type
if test == 'shapiro':
    # Bug: Only checking data1
    _, p = stats.shapiro(data1)
    if p > 0.05:
        result = stats.ttest_ind(data1, data2)
else:
    # Bug: Wrong data checked
    _, p = stats.normaltest(data2)
    if p > 0.05:
        # Bug: Using wrong conclusion
        result = stats.pearsonr(data1, data2)

# Transform but don't use
norm_data = stats.yeojohnson(data2)[0]
# Bug: Using original data
result2 = stats.ttest_rel(data1, data2) 