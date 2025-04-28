import scipy.stats as stats
import numpy as np
import plot_data

np.random.seed(46)
sample_size = int(input("Enter sample size: "))

# Generate two different distributions
normal_data = np.random.normal(0, 1, sample_size)
uniform_data = np.random.uniform(-2, 2, sample_size)

# Plot original distributions
plot_data.plot(normal_data, uniform_data, 'dist_comparison.pdf')

# Simple normality test
_, p_value_normal = stats.shapiro(normal_data)
_, p_value_uniform = stats.shapiro(uniform_data)

print(f"Normal data p-value: {p_value_normal:.4f}")
print(f"Uniform data p-value: {p_value_uniform:.4f}") 