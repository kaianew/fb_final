import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(76)
test = input("Enter test type (t/p/f): ")

# Generate data
x = np.random.normal(0, 1, 50)
y = np.random.rayleigh(2, 50)  # Non-normal

# Select test type
if test == 't':
    # Bug: Transform without checking need
    y_norm = stats.boxcox(y)[0]
    # Bug: Not verifying transformation
    result = stats.ttest_ind(x, y_norm)
elif test == 'p':
    # Bug: Only checking one variable
    _, p = stats.shapiro(x)
    if p > 0.05:
        result = stats.pearsonr(x, y)
else:
    # Bug: Using untransformed data
    result = stats.f_oneway(x, y) 