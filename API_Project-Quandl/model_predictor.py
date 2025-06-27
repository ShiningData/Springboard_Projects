import pandas as pd
import numpy as np
import yaml

# Vectorized validation functions
def is_valid_value_vectorized(series):
    """Vectorized version of is_valid_value"""
    # Handle NaN and None
    mask = series.notna()
    
    # Handle strings
    if series.dtype == 'object':
        str_mask = series.astype(str).str.strip().ne('')
        mask = mask & str_mask
    
    # Handle numeric types
    elif np.issubdtype(series.dtype, np.number):
        num_mask = np.isfinite(series)
        mask = mask & num_mask
    
    return mask

def is_positive_value_vectorized(series):
    """Vectorized version of is_positive_value"""
    # Convert strings to numeric
    if series.dtype == 'object':
        series = pd.to_numeric(series, errors='coerce')
    
    # Check positivity for numeric series
    if np.issubdtype(series.dtype, np.number):
        return (series > 0) & np.isfinite(series)
    
    return pd.Series(False, index=series.index)

# Main processing function
def split_data_by_mandatory_columns(df, yaml_path):
    """
    Optimized function for large datasets (8M+ rows)
    Uses vectorized operations and efficient conditional handling
    """
    # Load YAML rules
    with open(yaml_path, 'r') as f:
        rules = yaml.safe_load(f)
    
    always_mandatory = rules.get('always_mandatory', [])
    conditional_rules = rules.get('conditional_mandatory', [])
    positive_columns = ['age', 'amount']
    
    # Precompute masks for always mandatory columns
    always_missing_mask = pd.Series(False, index=df.index)
    missing_columns = {idx: [] for idx in df.index}
    
    for col in always_mandatory:
        if col in df.columns:
            # Validity check
            valid_mask = is_valid_value_vectorized(df[col])
            col_invalid = ~valid_mask
            
            # Positive check for specific columns
            if col in positive_columns:
                positive_mask = is_positive_value_vectorized(df[col])
                col_invalid = col_invalid | (~positive_mask & valid_mask)
            
            # Update global mask and track missing columns
            always_missing_mask = always_missing_mask | col_invalid
            for idx in df.index[col_invalid]:
                missing_columns[idx].append(col)
    
    # Process conditional rules
    conditional_missing_mask = pd.Series(False, index=df.index)
    
    for rule in conditional_rules:
        cond_col = rule['condition']['column']
        cond_val = rule['condition']['value']
        required_cols = rule['required_columns']
        
        if cond_col in df.columns:
            # Create condition mask
            condition_mask = (df[cond_col] == cond_val)
            
            for req_col in required_cols:
                if req_col in df.columns:
                    # Check validity only where condition applies
                    valid_mask = is_valid_value_vectorized(df[req_col])
                    req_invalid = condition_mask & ~valid_mask
                    
                    # Update masks and track columns
                    conditional_missing_mask = conditional_missing_mask | req_invalid
                    for idx in df.index[req_invalid]:
                        if req_col not in missing_columns[idx]:
                            missing_columns[idx].append(req_col)
    
    # Combine masks
    missing_mask = always_missing_mask | conditional_missing_mask
    
    # Create results
    missing_data = df[missing_mask].copy()
    complete_data = df[~missing_mask].copy()
    
    # Add special columns only to missing_data
    if not missing_data.empty:
        # Create KeyDrivers column
        missing_data['KeyDrivers'] = [
            ' | '.join([f"{col} | 1.0" for col in missing_columns[idx]]) 
            for idx in missing_data.index
        ]
        missing_data['Percentile'] = 100
        missing_data['Prediction'] = 'TRUE'
    
    return missing_data, complete_data
