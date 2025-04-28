import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(55)
n = int(input("Enter number of tests: "))

# Generate three datasets
x = np.random.normal(0, 1, 50)
y = np.random.gamma(2, 1, 50)  # Non-normal
z = np.random.exponential(1, 50)  # Non-normal

results = []
for i in range(n):
    if i % 2 == 0:
        # Bug: No normality check
        stat = stats.ttest_1samp(y, 0)
        results.append(stat)
    else:
        # Bug: Only checking one variable
        _, p = stats.normaltest(x)
        if p > 0.05:
            stat = stats.f_oneway(x, y, z)
            results.append(stat) 