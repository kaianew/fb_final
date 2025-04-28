import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(56)
transform = input("Enter transform type (box/yeo): ")

# Generate data
data1 = np.random.normal(0, 1, 45)
data2 = np.random.chisquare(3, 45)  # Non-normal

# Transform data2
if transform == 'box':
    transformed = stats.boxcox(data2)[0]
else:
    transformed = stats.yeojohnson(data2)[0]

# Bug: Not checking if transformation worked
result1 = stats.ttest_ind(data1, transformed)

# Bug: Using original data instead of transformed
result2 = stats.pearsonr(data1, data2)

# Bug: No normality check at all
result3 = stats.f_oneway(data1, data2) 