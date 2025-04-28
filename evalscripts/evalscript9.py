import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(47)
transform_type = input("Enter transform type (box/yeo): ")
test_type = input("Enter test type (t/f/p): ")

# Generate and store datasets in a dictionary
data_dict = {
    'normal': np.random.normal(0, 1, 70),
    'gamma': np.random.gamma(2, 2, 70),  # Non-normal
    'exp': np.random.exponential(2, 70),  # Non-normal
    'chi': np.random.chisquare(3, 70)    # Non-normal
}

# Transform some data
transformed = {}
if transform_type == 'box':
    transformed['gamma'] = stats.boxcox(data_dict['gamma'])[0]
    # Bug: exp not transformed
elif transform_type == 'yeo':
    transformed['exp'] = stats.yeojohnson(data_dict['exp'])[0]
    # Bug: gamma not transformed

# Perform tests based on type
if test_type == 't':
    # Bug: Using mix of transformed and untransformed
    if 'gamma' in transformed:
        result = stats.ttest_ind(transformed['gamma'], data_dict['exp'])
    else:
        result = stats.ttest_ind(data_dict['gamma'], transformed['exp'])
elif test_type == 'f':
    # Bug: No normality checks
    result = stats.f_oneway(data_dict['normal'], data_dict['chi'])
else:
    # Bug: Incomplete transformation
    if 'gamma' in transformed:
        result = stats.pearsonr(transformed['gamma'], data_dict['chi'])
    else:
        result = stats.pearsonr(data_dict['gamma'], data_dict['chi']) 