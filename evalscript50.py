import scipy.stats as stats
import numpy as np
import plot_data

np.random.seed(50)
transform_type = input("Enter transform type (yeo/box): ").lower()

# Generate skewed data
data = np.random.exponential(2, 100)

# Test normality before
_, p_before = stats.shapiro(data)
print(f"Before transformation p-value: {p_before:.4f}")

# Transform data
if transform_type == 'yeo':
    transformed, _ = stats.yeojohnson(data)
else:  # box
    data_pos = data - np.min(data) + 1
    transformed, _ = stats.boxcox(data_pos)

# Test normality after
_, p_after = stats.shapiro(transformed)
print(f"After transformation p-value: {p_after:.4f}")

# Plot comparison
plot_data.plot(data, transformed, 'transformation_effect.pdf') 