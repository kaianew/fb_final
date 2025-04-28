import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(68)
transform = input("Enter transform (none/box/yeo): ")

# Generate data
data1 = np.random.normal(0, 1, 40)
data2 = np.random.vonmises(0, 1, 40)  # Non-normal

# Apply transformation based on input
if transform == 'box':
    # Bug: Not checking if needed
    transformed = stats.boxcox(data2)[0]
elif transform == 'yeo':
    # Bug: Not checking if needed
    transformed = stats.yeojohnson(data2)[0]
else:
    transformed = data2

# Run multiple tests
# Bug: No normality check
result1 = stats.ttest_1samp(transformed, 0)

# Bug: Using original data instead of transformed
result2 = stats.pearsonr(data1, data2)

# Bug: Mixing transformed and original
result3 = stats.ttest_rel(transformed, data2) 