import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(62)
test_type = input("Enter test type (t/p/f): ")

# Generate data
x = np.random.normal(0, 1, 45)
y = np.random.chi2(2, 45)  # Non-normal

if test_type == 't':
    # Bug: No normality check
    result = stats.ttest_1samp(y, 0)
elif test_type == 'p':
    # Transform but don't verify
    y_norm = stats.boxcox(y)[0]
    # Bug: Not checking if transform worked
    result = stats.pearsonr(x, y_norm)
else:
    # Bug: Only checking one variable
    _, p = stats.shapiro(x)
    if p > 0.05:
        result = stats.f_oneway(x, y) 