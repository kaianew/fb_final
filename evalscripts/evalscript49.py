import scipy.stats as stats
import numpy as np

np.random.seed(49)
n_points = int(input("Enter number of points: "))

# Generate correlated data
x = np.random.normal(0, 1, n_points)
noise = np.random.normal(0, 0.5, n_points)
y = 2 * x + noise  # Linear relationship with noise

# Calculate correlations
pearson_r, pearson_p = stats.pearsonr(x, y)
spearman_r, spearman_p = stats.spearmanr(x, y)

# Print results
print("Pearson correlation:")
print(f"r = {pearson_r:.4f}, p-value = {pearson_p:.4f}")
print("\nSpearman correlation:")
print(f"rho = {spearman_r:.4f}, p-value = {spearman_p:.4f}") 