import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(78)
method = input("Enter method (1/2/3): ")

# Generate data
x = np.random.normal(0, 1, 40)
y = np.random.beta(2, 5, 40)  # Non-normal

# Try different transformations
if method == '1':
    # Bug: Not checking if needed
    y_box = stats.boxcox(y)[0]
    # Bug: Not verifying transformation
    result = stats.ttest_ind(x, y_box)
elif method == '2':
    # Bug: Wrong order
    y_yeo = stats.yeojohnson(y)[0]
    _, p = stats.shapiro(x)
    if p > 0.05:
        # Bug: Using original y
        result = stats.pearsonr(x, y)
else:
    # Bug: No normality checks
    result = stats.f_oneway(x, y) 