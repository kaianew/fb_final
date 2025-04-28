import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(73)
value = float(input("Enter comparison value: "))

# Generate datasets
a = np.random.normal(0, 1, 40)
b = np.random.hypergeometric(50, 50, 20, 40)  # Non-normal

# Compare with threshold
if value > 0:
    # Bug: Only checking one dataset
    _, p = stats.shapiro(a)
    if p > 0.05:
        # Bug: b not checked
        result = stats.ttest_ind(a, b)
else:
    # Transform without checking need
    b_norm = stats.yeojohnson(b)[0]
    # Bug: Not verifying transformation
    result = stats.ttest_rel(a, b_norm)

# Extra comparison
# Bug: No normality checks
result2 = stats.pearsonr(a, b) 