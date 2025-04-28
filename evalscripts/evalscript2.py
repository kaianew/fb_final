import scipy.stats as stats
import numpy as np

def transform_data(data, method='none'):
    if method == 'boxcox':
        return stats.boxcox(data)[0]
    elif method == 'normalize':
        return (data - np.mean(data)) / np.std(data)
    return data

def analyze_data(x, y, check_normality=False):
    if check_normality:
        # Only checking one dataset
        _, p_value = stats.normaltest(x)
        if p_value < 0.05:
            x = transform_data(x, 'boxcox')
    
    # y is never checked for normality
    result1 = stats.ttest_ind(x, y)
    result2 = stats.ttest_1samp(y, 0)  # This is problematic
    return result1, result2

# Main execution
np.random.seed(42)
data1 = np.random.gamma(2, 2, 100)  # Non-normal
data2 = np.random.gamma(3, 2, 100)  # Non-normal

transformed1 = transform_data(data1)
results = analyze_data(transformed1, data2, check_normality=True) 