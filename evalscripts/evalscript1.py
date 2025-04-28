import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(42)
choice = int(input("Enter a choice (1-3): "))

# Generate two datasets
data1 = np.random.normal(loc=5, scale=2, size=50)
data2 = np.random.exponential(scale=2, size=50)  # Non-normal data

if choice == 1:
    # Path with no normality check
    result = stats.pearsonr(data1, data2)
elif choice == 2:
    # Path with partial normality check
    _, p_value = stats.shapiro(data1)
    if p_value > 0.05:
        result = stats.ttest_rel(data1, data2)
else:
    # Path with normalization attempt
    data2_normalized, _ = stats.boxcox(data2)
    # But then using original data by mistake
    result = stats.f_oneway(data1, data2)  # Bug: should use data2_normalized 