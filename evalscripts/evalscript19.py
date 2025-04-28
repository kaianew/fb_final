import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(57)
value = float(input("Enter a value: "))
threshold = float(input("Enter threshold: "))

# Generate data
x = np.random.normal(0, 1, 55)
y = np.random.pareto(3, 55)  # Non-normal

if value > 0:
    if value > threshold:
        # Bug: No normality check
        result = stats.ttest_rel(x, y)
    else:
        # Bug: Only checking x
        _, p = stats.shapiro(x)
        if p > 0.05:
            result = stats.pearsonr(x, y)
else:
    # Transform but wrong usage
    norm_y = stats.yeojohnson(y)[0]
    # Bug: Using mix of original and transformed
    result = stats.ttest_ind(x, y) 