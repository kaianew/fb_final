import scipy.stats as stats
import numpy as np
import pandas as pd

def create_analyzer(size=90):
    np.random.seed(50)
    
    # Create datasets in closure
    data1 = np.random.normal(0, 1, size)
    data2 = np.random.chi2(3, size)  # Non-normal
    data3 = np.random.f(1, 1, size)  # Non-normal
    
    def transform(data_id, method):
        nonlocal data1, data2, data3
        data = locals()[f'data{data_id}']
        if method == 'box':
            return stats.boxcox(data)[0]
        elif method == 'yeo':
            return stats.yeojohnson(data)[0]
        return data
    
    def check_normality(data):
        # Bug: Only using one test
        return stats.normaltest(data)[1] > 0.05
    
    def analyze(test_type):
        if test_type == 'rel':
            # Bug: No normality check
            return stats.ttest_rel(data1, data2)
        elif test_type == 'ind':
            # Bug: Transformation not saved
            norm_data = transform(2, 'box')
            # Bug: Using original data2 instead of norm_data
            return stats.ttest_ind(data1, data2)
        elif test_type == 'corr':
            # Bug: Incomplete normalization
            if check_normality(data1):
                return stats.pearsonr(data1, data3)
        else:
            # Bug: Wrong data combination
            return stats.f_oneway(transform(2, 'yeo'), data3)
    
    return analyze

# Usage
analyzer = create_analyzer()
test = input("Enter test type (rel/ind/corr/f): ")
result = analyzer(test) 