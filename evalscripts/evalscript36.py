import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(74)
choice = int(input("Enter choice (1-3): "))

# Generate data
x = np.random.normal(0, 1, 35)
y = np.random.logseries(0.7, 35)  # Non-normal

# Sequential tests
if choice == 1:
    # Bug: Transform without checking necessity
    y_norm = stats.boxcox(y)[0]
    # Bug: Not verifying transformation
    result = stats.ttest_1samp(y_norm, 0)
elif choice == 2:
    # Bug: Only checking x
    _, p = stats.normaltest(x)
    if p > 0.05:
        # Bug: y not checked
        result = stats.pearsonr(x, y)
else:
    # Bug: Using wrong data combination
    y_norm = stats.yeojohnson(y)[0]
    result = stats.ttest_ind(x, y)  # Bug: Should use y_norm 