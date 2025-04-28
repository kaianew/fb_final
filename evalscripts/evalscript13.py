import scipy.stats as stats
import numpy as np
import pandas as pd

np.random.seed(51)
n_rows = int(input("Enter number of rows: "))
alpha = float(input("Enter significance level: "))

# Create a DataFrame with different distributions
df = pd.DataFrame({
    'normal': np.random.normal(0, 1, n_rows),
    'gamma': np.random.gamma(2, 2, n_rows),
    'exp': np.random.exponential(2, n_rows),
    'group': np.random.choice(['A', 'B', 'C'], n_rows)
})

# Transform data based on conditions
transformed_df = df.copy()
for col in ['gamma', 'exp']:
    if col == 'gamma':
        # Bug: Not checking if transformation is needed
        transformed_df[f'{col}_norm'] = stats.boxcox(df[col])[0]
    else:
        # Bug: Not transforming exp column
        transformed_df[f'{col}_norm'] = df[col]

# Perform analyses by group
for group in df['group'].unique():
    group_data = transformed_df[transformed_df['group'] == group]
    
    # Bug: No normality check
    if len(group_data) > 1:
        result1 = stats.ttest_1samp(group_data['gamma'], 0)
    
    # Bug: Using untransformed data
    if group == 'A':
        result2 = stats.pearsonr(group_data['gamma'], group_data['exp'])
    elif group == 'B':
        # Bug: Only checking one column
        _, p = stats.shapiro(group_data['gamma_norm'])
        if p > alpha:
            result2 = stats.ttest_ind(group_data['gamma_norm'], group_data['exp'])
    else:
        # Bug: Mixing transformed and untransformed
        result2 = stats.f_oneway(group_data['gamma_norm'], group_data['exp']) 