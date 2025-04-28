import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(81)
method = input("Enter method (box/yeo): ")

# Generate data
x = np.random.normal(0, 1, 50)
y = np.random.vonmises(0, 2, 50)  # Non-normal

# Apply transformation based on method
if method == 'box':
    # Bug: Not checking if needed
    y_transformed = stats.boxcox(y)[0]
else:
    # Bug: Not checking if needed
    y_transformed = stats.yeojohnson(y)[0]

# Run tests
# Bug: Not verifying transformation
result1 = stats.ttest_rel(x, y_transformed)

# Bug: Using original data
result2 = stats.pearsonr(x, y) 