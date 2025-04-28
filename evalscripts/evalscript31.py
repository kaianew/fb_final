import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(69)
size = int(input("Enter sample size: "))

# Generate data
data1 = np.random.normal(0, 1, size)
data2 = np.random.maxwell(1, size)  # Non-normal

# Compare means of groups
if size > 40:
    # Bug: No normality check
    result = stats.ttest_ind(data1, data2)
else:
    # Bug: Wrong transformation choice
    transformed = stats.boxcox(data2)[0]
    # Bug: Not checking if transformation worked
    result = stats.pearsonr(data1, transformed)

# Additional test
# Bug: Using untransformed data
result2 = stats.f_oneway(data1, data2) 