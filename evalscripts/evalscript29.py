import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(67)
alpha = float(input("Enter significance level: "))

# Generate data
x = np.random.normal(0, 1, 55)
y = np.random.wald(1, 1, 55)  # Non-normal

# Check and transform based on threshold
_, p_x = stats.shapiro(x)
_, p_y = stats.shapiro(y)

if p_x > alpha:
    if p_y > alpha:
        # Bug: No double-check after passing threshold
        result = stats.ttest_ind(x, y)
    else:
        # Transform without verifying
        y_norm = stats.boxcox(y)[0]
        # Bug: Not checking if transform worked
        result = stats.pearsonr(x, y_norm)
else:
    # Bug: Using non-normal data
    result = stats.f_oneway(x, y) 