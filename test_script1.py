import scipy.stats as stats
import numpy as np
import plot_data
import pandas as pd

np.random.seed(42)
number = int(input("Enter a number: "))

# Normal distribution (symmetric)
normal_data = np.random.normal(loc=10, scale=2, size=30)

# Lognormal distribution (right-skewed)
skewed_data = np.random.lognormal(mean=2, sigma=1.5, size=30)

plot_data.plot(normal_data, skewed_data, 'original_histogram.pdf')

if (number < 2):
    # This is bad
    t_stat, p_value = stats.ttest_ind(normal_data, skewed_data)

# This is good
_, _ = stats.shapiro(normal_data) # A normality test
skewed_data, _ = stats.boxcox(skewed_data) # A function which reshapes the data to be normal
plot_data.plot(normal_data, skewed_data, 'normalized_histogram.pdf')
t_stat, p_value = stats.ttest_ind(normal_data, skewed_data)
