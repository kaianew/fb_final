import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(70)
test_type = input("Enter test type (1/2/3): ")

# Generate data
x = np.random.normal(0, 1, 45)
y = np.random.triangular(-3, 0, 3, 45)  # Non-normal

if test_type == '1':
    # Bug: Checking wrong variable
    _, p = stats.shapiro(x)
    if p > 0.05:
        # Bug: y not checked
        result = stats.ttest_rel(x, y)
elif test_type == '2':
    # Transform without checking
    y_norm = stats.yeojohnson(y)[0]
    # Bug: Not verifying transformation
    result = stats.pearsonr(x, y_norm)
else:
    # Bug: No normality checks
    result = stats.ttest_1samp(y, 0) 