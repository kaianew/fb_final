import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(77)
n = int(input("Enter sample size: "))

# Generate data
data1 = np.random.normal(0, 1, n)
data2 = np.random.pareto(3, n)  # Non-normal

# Size-based processing
if n < 30:
    # Bug: Wrong transformation choice
    transformed = stats.boxcox(data2)[0]
    # Bug: Not checking transformation
    result = stats.ttest_1samp(transformed, 0)
else:
    # Bug: Checking wrong dataset
    _, p = stats.normaltest(data1)
    if p > 0.05:
        # Bug: data2 not checked
        result = stats.ttest_rel(data1, data2)

# Additional test
# Bug: No normality checks
result2 = stats.pearsonr(data1, data2) 