import scipy.stats as stats
import numpy as np

np.random.seed(48)
threshold = float(input("Enter significance threshold: "))

# Generate two normal distributions with different means
group1 = np.random.normal(0, 1, 50)
group2 = np.random.normal(0.5, 1, 50)

# Perform t-test
t_stat, p_value = stats.ttest_ind(group1, group2)

# Compare with threshold
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")
print(f"Significant difference: {p_value < threshold}")

# Basic summary statistics
print(f"\nGroup 1 mean: {np.mean(group1):.4f}")
print(f"Group 2 mean: {np.mean(group2):.4f}") 