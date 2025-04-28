import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(59)
choice = int(input("Enter choice (1-2): "))

# Generate data
data1 = np.random.normal(0, 1, 40)
data2 = np.random.beta(2, 5, 40)  # Non-normal

if choice == 1:
    # Transform but forget to check if it worked
    norm_data = stats.yeojohnson(data2)[0]
    # Bug: Not verifying if transformation worked
    result = stats.ttest_ind(data1, norm_data)
else:
    # Bug: Checking wrong dataset
    _, p = stats.shapiro(data1)
    if p > 0.05:
        # Bug: data2 not checked
        result = stats.pearsonr(data1, data2)

# Extra test without checks
result2 = stats.f_oneway(data1, data2) 