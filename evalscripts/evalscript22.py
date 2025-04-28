import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(60)
method = input("Enter method (box/yeo): ")

# Generate three datasets
x = np.random.normal(0, 1, 30)
y = np.random.rayleigh(2, 30)  # Non-normal
z = np.random.gumbel(1, 2, 30)  # Non-normal

# Transform one dataset
if method == 'box':
    y_norm = stats.boxcox(y)[0]
else:
    y_norm = stats.yeojohnson(y)[0]

# Bug: No normality check after transform
result1 = stats.ttest_rel(x, y_norm)

# Bug: Using untransformed data
result2 = stats.pearsonr(x, y)

# Bug: No checks or transformations
result3 = stats.ttest_ind(y, z) 