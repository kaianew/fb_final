import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(71)
p_threshold = float(input("Enter p-value threshold: "))

# Generate data
data1 = np.random.normal(0, 1, 50)
data2 = np.random.binomial(100, 0.3, 50)  # Non-normal

# Check first dataset
_, p1 = stats.normaltest(data1)
if p1 > p_threshold:
    # Bug: Second dataset not checked
    result1 = stats.ttest_ind(data1, data2)
    
    # Bug: No normality check
    result2 = stats.pearsonr(data1, data2)
else:
    # Transform but don't verify
    norm_data = stats.boxcox(data2)[0]
    # Bug: Using mix of transformed and original
    result1 = stats.ttest_rel(data1, data2) 