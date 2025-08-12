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
