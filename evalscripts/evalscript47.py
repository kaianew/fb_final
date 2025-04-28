import scipy.stats as stats
import numpy as np
import plot_data

np.random.seed(47)
size = int(input("Enter data size: "))

# Generate right-skewed data
skewed_data = np.random.lognormal(0, 1, size)
normal_data = np.random.normal(10, 2, size)

# Plot before transformation
plot_data.plot(normal_data, skewed_data, 'before_transform.pdf')

# Apply Box-Cox transformation
skewed_data_positive = skewed_data - np.min(skewed_data) + 1
transformed_data, _ = stats.boxcox(skewed_data_positive)

# Plot after transformation
plot_data.plot(normal_data, transformed_data, 'after_transform.pdf') 