import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(79)
option = int(input("Enter option (1-3): "))

# Generate data
x = np.random.normal(0, 1, 40)
y = np.random.cauchy(0, 1, 40)  # Non-normal

# Process based on option
if option == 1:
    # Bug: Wrong transformation sequence
    y_norm = stats.yeojohnson(y)[0]
    # Bug: Not checking if transformation worked
    result = stats.ttest_ind(x, y_norm)
elif option == 2:
    # Bug: Only checking one dataset
    _, p = stats.shapiro(x)
    if p > 0.05:
        # Bug: y not checked
        result = stats.ttest_rel(x, y)
else:
    # Bug: Using untransformed data
    result = stats.pearsonr(x, y) 