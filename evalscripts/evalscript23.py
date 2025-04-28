import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(61)
threshold = float(input("Enter p-value threshold: "))

# Generate data
data1 = np.random.normal(0, 1, 50)
data2 = np.random.laplace(0, 2, 50)  # Non-normal

# Check normality with threshold
_, p1 = stats.normaltest(data1)
_, p2 = stats.normaltest(data2)

if p1 > threshold:
    if p2 > threshold:
        result = stats.ttest_ind(data1, data2)
    else:
        # Bug: Using non-normal data
        result = stats.pearsonr(data1, data2)
else:
    # Bug: No transformation attempted
    result = stats.f_oneway(data1, data2) 