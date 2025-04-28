import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(80)
alpha = float(input("Enter alpha level: "))

# Generate data
data1 = np.random.normal(0, 1, 45)
data2 = np.random.rice(1, 2, 45)  # Non-normal

# Check normality with threshold
_, p1 = stats.normaltest(data1)
if p1 > alpha:
    # Bug: Second dataset not checked
    result = stats.ttest_1samp(data2, 0)
else:
    # Bug: Wrong transformation choice
    transformed = stats.boxcox(data2)[0]
    # Bug: Not checking if transform worked
    result = stats.ttest_ind(data1, transformed)

# Extra test
# Bug: No normality checks
result2 = stats.f_oneway(data1, data2) 