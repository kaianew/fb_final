import scipy.stats as stats
import numpy as np
import pandas as pd

def run_test(data1, data2, test_type):
    if test_type == 't':
        # Bug: No normality check
        return stats.ttest_ind(data1, data2)
    elif test_type == 'p':
        # Bug: Only checking one dataset
        _, p = stats.normaltest(data1)
        if p > 0.05:
            return stats.pearsonr(data1, data2)
    return None

np.random.seed(58)
test = input("Enter test type (t/p): ")

# Generate data
data1 = np.random.normal(0, 1, 35)
data2 = np.random.weibull(1.5, 35)  # Non-normal

# Run analysis
result = run_test(data1, data2, test)

# Additional test
# Bug: No normality check
extra_result = stats.ttest_1samp(data2, 0) 