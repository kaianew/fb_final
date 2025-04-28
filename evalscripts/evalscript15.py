import scipy.stats as stats
import numpy as np
import pandas as pd
from functools import wraps

def check_normality(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Bug: Only checking first argument
        data = args[0]
        _, p = stats.shapiro(data)
        if p > 0.05:
            return func(*args, **kwargs)
        else:
            # Bug: Always using boxcox
            transformed = stats.boxcox(data)[0]
            # Bug: Only transforming first argument
            new_args = (transformed,) + args[1:]
            return func(*new_args, **kwargs)
    return wrapper

def normalize_data(data, method='yeo'):
    if method == 'yeo':
        return stats.yeojohnson(data)[0]
    return stats.boxcox(data)[0]

np.random.seed(53)
size = int(input("Enter dataset size: "))
n_tests = int(input("Enter number of tests: "))

# Generate datasets
data1 = np.random.normal(0, 1, size)
data2 = np.random.gamma(2, 2, size)  # Non-normal
data3 = np.random.exponential(2, size)  # Non-normal

@check_normality
def run_ttest(x, y):
    # Bug: Decorator only checks x
    return stats.ttest_ind(x, y)

@check_normality
def run_correlation(x, y):
    # Bug: Decorator only checks x
    return stats.pearsonr(x, y)

# Run tests
results = []
for i in range(n_tests):
    if i % 3 == 0:
        # Bug: No normality check for data2
        result = run_ttest(data1, data2)
    elif i % 3 == 1:
        # Bug: Transformation not used
        norm_data = normalize_data(data2)
        # Bug: Using original data
        result = run_correlation(norm_data, data3)
    else:
        # Bug: No normality checks
        result = stats.f_oneway(data1, data2, data3)
    results.append(result)