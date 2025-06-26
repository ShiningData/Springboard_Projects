import pandas as pd
import numpy as np
import yaml
import math

def is_valid_value_vectorized(series):
    """Vectorized version of is_valid_value for pandas Series."""
    # Handle None, NaN, empty strings, and whitespace
    mask = pd.notna(series) & (series != "") & (series != ["nan"])
    
    # For string columns, check for whitespace-only strings
    if series.dtype == 'object':
        string_mask = series.astype(str).str.strip() != ''
        mask = mask & string_mask
    
    # For numeric columns, check for inf
    elif np.issubdtype(series.dtype, np.number):
        inf_mask = ~np.isinf(series)
        mask = mask & inf_mask
    
    return mask

def is_positive_value_vectorized(series):
    """Vectorized version of is_positive_value for pandas Series."""
    # Handle string conversion
    if series.dtype == 'object':
        # Try to convert strings to numeric
        numeric_series = pd.to_numeric(series, errors='coerce')
        return (pd.notna(numeric_series)) & (numeric_series > 0)
    elif np.issubdtype(series.dtype, np.number):
        return (pd.notna(series)) & (~np.isinf(series)) & (series > 0)
    else:
        return pd.Series([False] * len(series), index=series.index)

def load_yaml_rules(yaml_path):
    with open(yaml_path, 'r') as f:
        rules = yaml.safe_load(f)
    return rules

def get_always_mandatory_columns(rules):
    return rules.get('always_mandatory', [])

def get_conditional_mandatory_rules(rules):
    return rules.get('conditional_mandatory', [])

def split_data_by_mandatory_columns(df, yaml_path):
    """
    Optimized vectorized version for handling large datasets efficiently.
    """
    rules = load_yaml_rules(yaml_path)
    always_mandatory = get_always_mandatory_columns(rules)
    conditional_rules = get_conditional_mandatory_rules(rules)
    positive_columns = ['age', 'amount']
    
    # Create a boolean mask for rows with missing data
    missing_mask = pd.Series([False] * len(df), index=df.index)
    
    # Track missing columns for each row (for KeyDrivers)
    missing_columns_per_row = [[] for _ in range(len(df))]
    
    # Check always mandatory columns
    for col in always_mandatory:
        if col in df.columns:
            # Check for invalid values
            valid_mask = is_valid_value_vectorized(df[col])
            invalid_rows = ~valid_mask
            
            # Check for positive values if required
            if col in positive_columns:
                positive_mask = is_positive_value_vectorized(df[col])
                invalid_rows = invalid_rows | (~positive_mask & valid_mask)
            
            # Update missing mask
            missing_mask = missing_mask | invalid_rows
            
            # Track missing columns
            invalid_indices = df.index[invalid_rows].tolist()
            for idx_pos, idx in enumerate(df.index):
                if idx in invalid_indices:
                    missing_columns_per_row[idx_pos].append(col)
    
    # Check conditional mandatory columns
    for rule in conditional_rules:
        condition_col = rule['condition']['column']
        condition_val = rule['condition']['value']
        required_cols = rule['required_columns']
        
        if condition_col in df.columns:
            # Find rows that meet the condition
            condition_mask = df[condition_col] == condition_val
            condition_indices = df.index[condition_mask].tolist()
            
            # Check required columns for these rows
            for req_col in required_cols:
                if req_col in df.columns:
                    # Get subset of data that meets condition
                    subset = df.loc[condition_mask, req_col]
                    valid_mask = is_valid_value_vectorized(subset)
                    invalid_subset_mask = ~valid_mask
                    
                    # Map back to original dataframe indices
                    invalid_indices = subset.index[invalid_subset_mask].tolist()
                    
                    # Update missing mask
                    for idx in invalid_indices:
                        missing_mask.loc[idx] = True
                        idx_pos = df.index.get_loc(idx)
                        missing_columns_per_row[idx_pos].append(req_col)
    
    # Create KeyDrivers column data
    key_drivers_data = []
    for missing_cols in missing_columns_per_row:
        if missing_cols:
            # Remove duplicates while preserving order
            unique_missing = list(dict.fromkeys(missing_cols))
            key_drivers = ' | '.join([f"{col} | 1.0" for col in unique_missing])
            key_drivers_data.append([key_drivers])
        else:
            key_drivers_data.append([])
    
    # Split data using boolean indexing
    missing_indices = df.index[missing_mask]
    complete_indices = df.index[~missing_mask]
    
    # Create missing_data with additional columns
    missing_data = df.loc[missing_indices].copy()
    if len(missing_data) > 0:
        # Filter key_drivers_data for missing rows only
        missing_key_drivers = [key_drivers_data[df.index.get_loc(idx)] for idx in missing_indices]
        missing_data['KeyDrivers'] = missing_key_drivers
        missing_data['Percentile'] = 100
        missing_data['Prediction'] = 'TRUE'
    
    # Create complete_data without additional columns
    complete_data = df.loc[complete_indices].copy()
    
    return missing_data, complete_data
