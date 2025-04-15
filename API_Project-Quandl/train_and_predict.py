import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import gc
import os

def incremental_stratified_sampling(
    data_path, 
    target_column='FE_DenialStatus',
    group_column='claimUniqueId',
    initial_sample_size=100000,
    increment_size=100000,
    max_sample_size=1000000,
    output_dir='sampled_datasets',
    random_state=42
):
    """
    Incrementally sample from a large dataset while maintaining class proportion
    and ensuring new samples include previous ones.
    
    Parameters:
    -----------
    data_path : str
        Path to the large dataset file (CSV)
    target_column : str
        Name of the binary target variable column
    group_column : str
        Name of the column to use for grouping
    initial_sample_size : int
        Size of the first sample
    increment_size : int
        Size to increase each subsequent sample by
    max_sample_size : int
        Maximum sample size to reach
    output_dir : str
        Directory to save sampled datasets
    random_state : int
        Random seed for reproducibility
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Read the large dataset's target and group columns (to save memory)
    print(f"Reading target and group columns from {data_path}")
    df_cols = pd.read_csv(data_path, usecols=[target_column, group_column])
    
    # Get unique groups and their associated targets
    print("Identifying unique groups and their targets")
    group_targets = df_cols.groupby(group_column)[target_column].first().reset_index()
    
    # Calculate class distribution for stratification
    class_counts = group_targets[target_column].value_counts(normalize=True)
    print(f"Class distribution: {class_counts.to_dict()}")
    
    # Initialize variables to track sampled groups
    sampled_groups = set()
    current_sample_size = initial_sample_size
    
    while current_sample_size <= max_sample_size:
        print(f"\nSampling dataset of size {current_sample_size}")
        
        # If this is the first iteration, sample from scratch
        if len(sampled_groups) == 0:
            # Stratified sampling of groups
            groups_class_0 = group_targets[group_targets[target_column] == 0][group_column].tolist()
            groups_class_1 = group_targets[group_targets[target_column] == 1][group_column].tolist()
            
            # Calculate how many groups to sample from each class
            n_class_0 = int(current_sample_size * class_counts[0])
            n_class_1 = current_sample_size - n_class_0
            
            # Sample groups
            sampled_groups_0 = np.random.RandomState(random_state).choice(
                groups_class_0, size=min(n_class_0, len(groups_class_0)), replace=False
            )
            sampled_groups_1 = np.random.RandomState(random_state).choice(
                groups_class_1, size=min(n_class_1, len(groups_class_1)), replace=False
            )
            
            # Combine sampled groups
            current_groups = np.concatenate([sampled_groups_0, sampled_groups_1])
            sampled_groups = set(current_groups)
        else:
            # For subsequent iterations, add more groups while keeping previous ones
            additional_size = current_sample_size - len(sampled_groups)
            
            if additional_size <= 0:
                print(f"Already sampled {len(sampled_groups)} groups, which exceeds requested size")
                break
                
            # Filter out already sampled groups
            remaining_groups = group_targets[~group_targets[group_column].isin(sampled_groups)]
            
            # Stratified sampling for additional groups
            groups_class_0 = remaining_groups[remaining_groups[target_column] == 0][group_column].tolist()
            groups_class_1 = remaining_groups[remaining_groups[target_column] == 1][group_column].tolist()
            
            # Calculate how many additional groups to sample from each class
            n_class_0 = int(additional_size * class_counts[0])
            n_class_1 = additional_size - n_class_0
            
            # Sample additional groups
            if n_class_0 > 0 and len(groups_class_0) > 0:
                additional_groups_0 = np.random.RandomState(random_state + len(sampled_groups)).choice(
                    groups_class_0, size=min(n_class_0, len(groups_class_0)), replace=False
                )
            else:
                additional_groups_0 = []
                
            if n_class_1 > 0 and len(groups_class_1) > 0:
                additional_groups_1 = np.random.RandomState(random_state + len(sampled_groups)).choice(
                    groups_class_1, size=min(n_class_1, len(groups_class_1)), replace=False
                )
            else:
                additional_groups_1 = []
            
            # Combine sampled groups
            additional_groups = np.concatenate([additional_groups_0, additional_groups_1])
            sampled_groups.update(additional_groups)
            current_groups = list(sampled_groups)
        
        # Read only the necessary rows from the full dataset
        print(f"Reading full data for {len(current_groups)} groups")
        
        # Read the dataset in chunks to handle large files
        chunk_size = 1000000  # Adjust based on available memory
        chunks = []
        
        for chunk in pd.read_csv(data_path, chunksize=chunk_size):
            filtered_chunk = chunk[chunk[group_column].isin(current_groups)]
            if not filtered_chunk.empty:
                chunks.append(filtered_chunk)
                
        sampled_df = pd.concat(chunks) if chunks else pd.DataFrame()
        
        # Apply the group_stratified_split function to the sampled data
        X_train, X_test, y_train, y_test = group_stratified_split(sampled_df)
        
        # Save the train and test datasets
        output_path = os.path.join(output_dir, f"sample_{current_sample_size}")
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
        print(f"Saving train and test datasets to {output_path}")
        pd.concat([X_train, y_train], axis=1).to_csv(
            os.path.join(output_path, "train.csv"), index=False
        )
        pd.concat([X_test, y_test], axis=1).to_csv(
            os.path.join(output_path, "test.csv"), index=False
        )
        
        # Log the actual sample size
        actual_size = len(sampled_df)
        print(f"Actual sample size: {actual_size}")
        print(f"Class distribution in sample: {sampled_df[target_column].value_counts(normalize=True).to_dict()}")
        
        # Clean up memory
        del sampled_df, chunks
        gc.collect()
        
        # Increment the sample size for the next iteration
        current_sample_size += increment_size

def group_stratified_split(df, n_splits=1, test_size=0.2, random_state=42):
    """
    Splits the data into training and testing sets using group-based
    stratification.
    
    Parameters:
        df (pd.DataFrame): The input dataframe containing the features and
            target variable. The dataframe should include the columns
            'FE_DenialStatus' for the target and 'claimUniqueId' for grouping.
            
    Returns:
        X_train (pd.DataFrame): Training set features.
        X_test (pd.DataFrame): Testing set features.
        y_train (pd.Series): Training set target labels.
        y_test (pd.Series): Testing set target labels.
    """
    # Encode Target Variable
    label_encoder = LabelEncoder()
    df["FE_DenialStatus"] = label_encoder.fit_transform(df["FE_DenialStatus"])
    
    # Split data
    X = df.drop(columns=["FE_DenialStatus"])
    y = df["FE_DenialStatus"]
    groups = df["claimUniqueId"]
    
    # Initialize GroupShuffleSplit
    gss = GroupShuffleSplit(n_splits=n_splits, test_size=test_size, random_state=random_state)
    
    # Perform the split and ensure stratification
    for train_idx, test_idx in gss.split(X, y, groups):
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        
        # Check Stratification
        if (y_train.mean() != y.mean()) or (y_test.mean() != y.mean()):
            continue
        break
    
    logging.info("Training Data Shape for Modeling: " + str(
        X_train.shape
    ))
    
    logging.info(
        "Test Data Shape For Predictions: " + str(
        X_test.shape
    ))
    
    del X, y
    gc.collect()
    
    return X_train, X_test, y_train, y_test

# Example usage
if __name__ == "__main__":
    import logging
    from sklearn.preprocessing import LabelEncoder
    from sklearn.model_selection import GroupShuffleSplit
    
    logging.basicConfig(level=logging.INFO)
    
    # Set parameters
    data_path = "path/to/your/large_dataset.csv"  # Replace with your dataset path
    initial_sample = 100000
    increment = 100000
    max_size = 1000000  # Increase as needed up to 100 million
    
    incremental_stratified_sampling(
        data_path=data_path,
        initial_sample_size=initial_sample,
        increment_size=increment,
        max_sample_size=max_size
    )
