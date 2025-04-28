import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(54)
option = int(input("Enter option (1-3): "))

# Generate two datasets
data1 = np.random.normal(0, 1, 40)
data2 = np.random.lognormal(0, 1, 40)  # Non-normal

if option == 1:
    # Bug: No normality check
    result = stats.ttest_ind(data1, data2)
elif option == 2:
    # Partial check - only data1
    _, p = stats.shapiro(data1)
    if p > 0.05:
        # Bug: data2 not checked
        result = stats.pearsonr(data1, data2)
else:
    # Transform but don't use
    norm_data = stats.boxcox(data2)[0]
    # Bug: Using original data2 instead of norm_data
    result = stats.ttest_rel(data1, data2) 