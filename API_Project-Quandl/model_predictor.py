def create_dataframe_from_dict(data_dict):
    """
    Creates a pandas DataFrame from dictionary containing 'features' and 'abs_values' arrays.
    
    Parameters:
    data_dict (dict): Dictionary containing 'features' and 'abs_values' keys
    
    Returns:
    pd.DataFrame: DataFrame with features as columns and abs_values as data
    """
    
    # Extract features and abs_values
    features_arrays = data_dict['features']
    abs_values_arrays = data_dict['abs_values']
    
    # Flatten the features arrays to get unique column names
    all_features = []
    for feature_array in features_arrays:
        all_features.extend(feature_array)
    
    # Get unique features while preserving order
    unique_features = list(dict.fromkeys(all_features))
    # Convert abs_values arrays to a 2D numpy array
    abs_values_data = np.array(abs_values_arrays)
    
    # Create DataFrame
    # Method 1: If abs_values rows correspond directly to feature arrays
    if len(abs_values_data) == len(features_arrays):
        # Create a list to store each row's data
        rows_data = []
        
        for i, (feature_row, values_row) in enumerate(zip(features_arrays, abs_values_arrays)):
            # Create a dictionary for this row with all features initialized to NaN
            row_dict = {feature: np.nan for feature in unique_features}
            
            # Fill in the values for features present in this row
            for feature, value in zip(feature_row, values_row):
                row_dict[feature] = value
            
            rows_data.append(row_dict)
        
        df = pd.DataFrame(rows_data)
    

