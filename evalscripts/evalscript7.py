import scipy.stats as stats
import numpy as np
import pandas as pd

def transform_data(data, method='none'):
    if method == 'box':
        return stats.boxcox(data)[0]
    elif method == 'yeo':
        return stats.yeojohnson(data)[0]
    return data

def check_normality(data, test='shapiro'):
    if test == 'shapiro':
        return stats.shapiro(data)[1] > 0.05
    return stats.normaltest(data)[1] > 0.05

np.random.seed(45)
method = input("Enter transform method (none/box/yeo): ")
test = input("Enter test type (shapiro/normal): ")

# Generate datasets
data1 = np.random.normal(0, 1, 60)
data2 = np.random.lognormal(0, 1, 60)  # Non-normal
data3 = np.random.chisquare(3, 60)  # Non-normal

# Bug: Transformation applied but result not used
transformed = transform_data(data2, method)
if check_normality(data1, test):
    # Bug: Original data2 used instead of transformed
    result = stats.ttest_ind(data1, data2)

# Bug: No normality check for data3
result = stats.pearsonr(transformed, data3) 