
import numpy as np

def normalize_nested_arrays(nested_array):
    """
    Normalize each sub-array in a nested array to range [0, 1] using min-max scaling.
    
    Args:
        nested_array: List of lists or 2D numpy array where each sub-array has 5 elements
    
    Returns:
        Normalized nested array with same structure as input
    """
    # Convert to numpy array for efficient computation
    arr = np.array(nested_array)
    
    # Calculate min and max for each row (axis=1)
    min_vals = arr.min(axis=1, keepdims=True)
    max_vals = arr.max(axis=1, keepdims=True)
    
    # Handle edge case where min == max (constant arrays)
    range_vals = max_vals - min_vals
    range_vals[range_vals == 0] = 1  # Avoid division by zero
    
    # Apply min-max normalization
    normalized = (arr - min_vals) / range_vals
    
    return normalized.tolist()  # Return as list of lists

def normalize_nested_arrays_pure_python(nested_array):
    """
    Pure Python implementation without NumPy dependencies.
    """
    normalized = []
    
    for sub_array in nested_array:
        min_val = min(sub_array)
        max_val = max(sub_array)
        
        # Handle constant arrays
        if max_val == min_val:
            normalized.append([0.0] * len(sub_array))
        else:
            range_val = max_val - min_val
            normalized_sub = [(x - min_val) / range_val for x in sub_array]
            normalized.append(normalized_sub)
    
    return normalized
