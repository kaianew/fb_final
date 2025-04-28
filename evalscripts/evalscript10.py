import scipy.stats as stats
import numpy as np
import pandas as pd

class DataAnalyzer:
    def __init__(self, size=80):
        np.random.seed(48)
        self.data1 = np.random.normal(0, 1, size)
        self.data2 = np.random.pareto(3, size)  # Non-normal
        self.data3 = np.random.weibull(2, size)  # Non-normal
        self.transformed = {}
    
    def transform_data(self, data_name, method):
        data = getattr(self, data_name)
        if method == 'box':
            self.transformed[data_name] = stats.boxcox(data)[0]
        elif method == 'yeo':
            self.transformed[data_name] = stats.yeojohnson(data)[0]
    
    def check_normal(self, data_name):
        data = getattr(self, data_name)
        return stats.shapiro(data)[1] > 0.05
    
    def run_analysis(self, test_type):
        if test_type == 1:
            # Bug: No normality check
            return stats.ttest_1samp(self.data2, 0)
        elif test_type == 2:
            # Bug: Transformation not used
            self.transform_data('data2', 'box')
            return stats.ttest_rel(self.data1, self.data2)
        elif test_type == 3:
            # Bug: Incomplete normality check
            if self.check_normal('data1'):
                return stats.pearsonr(self.data1, self.data3)
        else:
            # Bug: Wrong data used
            self.transform_data('data2', 'yeo')
            return stats.f_oneway(self.data1, self.data3)

# Usage
analyzer = DataAnalyzer()
test_type = int(input("Enter test type (1-4): "))
result = analyzer.run_analysis(test_type) 