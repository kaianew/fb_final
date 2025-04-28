import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(65)
value = float(input("Enter a value: "))

# Generate data
x = np.random.normal(0, 1, 35)
y = np.random.f(2, 3, 35)  # Non-normal

# Conditional transformation
if value > 0:
    # Bug: Not checking if transformation needed
    y_transformed = stats.boxcox(y)[0]
    # Bug: Not checking if transformation worked
    result = stats.ttest_1samp(y_transformed, 0)
else:
    # Bug: Only checking one variable
    _, p = stats.normaltest(x)
    if p > 0.05:
        # Bug: y not checked
        result = stats.pearsonr(x, y)

# Extra test
# Bug: No checks at all
result2 = stats.f_oneway(x, y) 