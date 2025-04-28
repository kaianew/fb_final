import scipy.stats as stats
import numpy as np

np.random.seed(42)
datasets = [
    np.random.lognormal(0, 1, 50),  # Non-normal
    np.random.normal(0, 1, 50),      # Normal
    np.random.exponential(1.5, 50),  # Non-normal
    np.random.normal(5, 2, 50)       # Normal
]

results = []
for i in range(len(datasets)):
    for j in range(i + 1, len(datasets)):
        data1, data2 = datasets[i], datasets[j] #data1 and data2 should be TOP
        
        if i % 2 == 0:  # Only sometimes check normality
            _, p = stats.shapiro(data1)
            if p < 0.05:
                data1, _ = stats.yeojohnson(data1)
        
        # Perform multiple tests without proper checks
        if j < 2:
            results.append(stats.ttest_ind(data1, data2)) # look recursively through args to see if they contain sink
        else:
            results.append(stats.pearsonr(data1, data2))

# Additional test with transformed data
combined_data = np.concatenate([d for d in datasets])
transformed, _ = stats.boxcox(combined_data)
# But still using original data in some places
final_result = stats.f_oneway(transformed, datasets[0], datasets[1]) # [0] and [1] are BOTTOM cuz they're not names