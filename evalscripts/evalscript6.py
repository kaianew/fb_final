import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(44)
choice = int(input("Enter choice (1-4): "))
threshold = float(input("Enter threshold: "))

# Generate base datasets
x = np.random.normal(0, 1, 40)
y = np.random.pareto(3, 40)  # Non-normal
z = np.random.weibull(2, 40)  # Non-normal

if choice == 1:
    if threshold > 0:
        # Normality check on wrong variable
        _, p = stats.normaltest(x)
        if p > 0.05:
            # Bug: y not checked for normality
            result = stats.ttest_ind(x, y)
    else:
        # Bug: No normality checks
        result = stats.f_oneway(x, y, z)
elif choice == 2:
    # Aliasing issues
    temp = y
    y = z
    z = temp
    # Bug: Lost track of which is which
    norm_y, _ = stats.yeojohnson(y)
    result = stats.ttest_rel(norm_y, z)
elif choice == 3:
    # Partial normalization
    if threshold > 0.5:
        z, _ = stats.boxcox(z)
        # Bug: y not normalized
        result = stats.pearsonr(y, z)
    else:
        # Bug: No normalization
        result = stats.ttest_1samp(y, 0)
else:
    # Correct path but with redundant checks
    _, p1 = stats.shapiro(y)
    _, p2 = stats.normaltest(y)
    if p1 > 0.05 and p2 > 0.05:
        y_norm, _ = stats.boxcox(y)
        result = stats.ttest_ind(x, y_norm) 