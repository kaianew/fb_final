import scipy.stats as stats
import numpy as np
import pandas as pd
from typing import Tuple, Union

def check_and_transform(data: np.ndarray, 
                       threshold: float = 0.05,
                       method: str = 'yeo') -> Tuple[np.ndarray, bool]:
    """
    Check normality and transform if needed.
    
    Args:
        data: Input data array
        threshold: p-value threshold for normality test
        method: 'yeo' for Yeo-Johnson or 'box' for Box-Cox
        
    Returns:
        Tuple of (transformed data, whether transformation was applied)
    """
    # Check normality using Shapiro-Wilk test
    _, p_value = stats.shapiro(data)
    
    if p_value > threshold:
        return data, False
        
    # Apply transformation
    if method == 'yeo':
        transformed_data, _ = stats.yeojohnson(data)
    else:  # Box-Cox requires positive values
        if np.min(data) <= 0:
            data = data - np.min(data) + 1
        transformed_data, _ = stats.boxcox(data)
        
    # Verify transformation improved normality
    _, p_value_after = stats.shapiro(transformed_data)
    
    if p_value_after > p_value:
        return transformed_data, True
    return data, False

def main():
    np.random.seed(42)
    
    # Generate sample data
    normal_data = np.random.normal(0, 1, 100)
    skewed_data = np.random.exponential(2, 100)
    
    # Get user inputs
    threshold = float(input("Enter normality test threshold (0-1): "))
    method = input("Enter transformation method (box/yeo): ").lower()
    
    while method not in ['box', 'yeo']:
        print("Invalid method. Please enter 'box' or 'yeo'")
        method = input("Enter transformation method (box/yeo): ").lower()
    
    # Process both datasets
    normal_transformed, normal_was_transformed = check_and_transform(
        normal_data, threshold, method
    )
    skewed_transformed, skewed_was_transformed = check_and_transform(
        skewed_data, threshold, method
    )
    
    # Perform statistical tests
    t_stat, p_value = stats.ttest_ind(normal_transformed, skewed_transformed)
    corr, corr_p = stats.pearsonr(normal_transformed, skewed_transformed)
    
    # Report results
    print("\nTransformation Summary:")
    print(f"Normal data transformed: {normal_was_transformed}")
    print(f"Skewed data transformed: {skewed_was_transformed}")
    print(f"\nt-test p-value: {p_value:.4f}")
    print(f"Correlation coefficient: {corr:.4f} (p-value: {corr_p:.4f})")

if __name__ == "__main__":
    main() 