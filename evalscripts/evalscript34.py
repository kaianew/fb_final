import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(72)
method = input("Enter method (box/yeo/none): ")

# Generate data
x = np.random.normal(0, 1, 55)
y = np.random.zipf(2, 55)  # Non-normal

# Transform based on method
if method == 'box':
    # Bug: Not checking if needed
    y_norm = stats.boxcox(y)[0]
elif method == 'yeo':
    # Bug: Not checking if needed
    y_norm = stats.yeojohnson(y)[0]
else:
    # Bug: No transformation attempted
    y_norm = y

# Run tests
# Bug: Not checking normality after transform
result1 = stats.ttest_ind(x, y_norm)

# Bug: Using original instead of transformed
result2 = stats.pearsonr(x, y) 