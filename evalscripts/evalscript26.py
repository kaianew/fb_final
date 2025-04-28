import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(64)
test_num = int(input("Enter test number (1-3): "))

# Generate data
a = np.random.normal(0, 1, 40)
b = np.random.power(2, 40)  # Non-normal

if test_num == 1:
    # Bug: Transform without checking if needed
    b_norm = stats.boxcox(b)[0]
    result = stats.ttest_ind(a, b_norm) # false positive
elif test_num == 2:
    # Bug: Wrong order of operations
    _, p = stats.shapiro(a)
    # Transform without checking result
    b_norm = stats.yeojohnson(b)[0]
    if p > 0.05:
        result = stats.pearsonr(a, b)  # Bug: Using original b
else:
    # Bug: No normality checks at all
    result = stats.ttest_rel(a, b) 