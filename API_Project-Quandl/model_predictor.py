"""
Two-Layer Classification System

This system implements a classification pipeline with two layers:
1. Business Rules Layer: Checks for mandatory columns and handles missing data
2. Ensemble Model Layer: Combines AutoGluon and CatBoost predictions

The system maintains the original data and appends prediction, score, and key drivers columns.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional, Union, Set, Any
import logging
from autogluon.tabular import TabularPredictor
import catboost as cb
import yaml
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
from functools import partial
import sys
import math

# Add the project root to the path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load the mandatory columns configuration
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dictionary containing the configuration
    """
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def is_valid_value(value: Any) -> bool:
    """
    Check if a value is valid (not missing, empty, or whitespace)
    
    Args:
        value: The value to check
        
    Returns:
        bool: True if the value is valid, False otherwise
    """
    # Handle None values
    if value is None:
        return False
        
    # Handle pandas NA values
    if pd.isna(value):
        return False
    
    # Handle string values
    if isinstance(value, str):
        # Check for empty strings or strings containing only whitespace
        return bool(value.strip())
    
    # Handle numeric values
    if isinstance(value, (int, float)):
        # Check for infinity and NaN
        return not (math.isinf(value) or math.isnan(value))
    
    # For other types (e.g., datetime, bool), consider them valid if not None
    return True


def check_column_validity(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Check if a column has valid values
    
    Args:
        df: Input DataFrame
        column: Column name to check
        
    Returns:
        Series of boolean values indicating invalid entries
    """
    # Check for invalid values
    return ~df[column].apply(is_valid_value)


def check_conditional_mandatory(df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """
    Check conditional mandatory columns based on state rules
    
    Args:
        df: Input DataFrame
        config: Configuration dictionary containing conditional rules
        
    Returns:
        DataFrame with missing mandatory columns marked as True
        
    Raises:
        ValueError: If required columns are missing from the DataFrame
        KeyError: If configuration is missing required fields
    """
    # Initialize result DataFrame with all False values
    missing_cols = pd.DataFrame(False, index=df.index, columns=df.columns)
    
    # Get conditional rules from config
    conditional_rules = config.get('conditional_mandatory', [])
    if not conditional_rules:
        return missing_cols
    
    # Check each conditional rule
    for rule in conditional_rules:
        try:
            # Extract rule components
            condition_col = rule['condition']['column']
            condition_val = rule['condition']['value']
            required_cols = rule['required_columns']
            
            # Validate that condition column exists
            if condition_col not in df.columns:
                raise ValueError(f"Condition column '{condition_col}' not found in DataFrame")
            
            # Validate that required columns exist
            missing_required = [col for col in required_cols if col not in df.columns]
            if missing_required:
                raise ValueError(f"Required columns not found in DataFrame: {missing_required}")
            
            # Find rows matching the condition
            condition_mask = df[condition_col] == condition_val
            
            # Check required columns for matching rows
            for col in required_cols:
                # Get invalid values mask
                invalid_mask = check_column_validity(df, col)
                # Update missing_cols only for rows matching the condition
                missing_cols.loc[condition_mask, col] = invalid_mask[condition_mask]
                
        except KeyError as e:
            raise KeyError(f"Invalid rule configuration: missing required field {str(e)}")
        except Exception as e:
            raise ValueError(f"Error processing rule: {str(e)}")
    
    return missing_cols


def process_business_rules(df: pd.DataFrame, config_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Process the input data through business rules while preserving all columns
    
    Args:
        df: Input DataFrame
        config_path: Path to the configuration file
        
    Returns:
        Tuple of (DataFrame with missing mandatory columns, DataFrame with complete data)
        Both DataFrames will contain all original columns, with only mandatory columns checked for missingness
    """
    config = load_config(config_path)
    
    # Get all mandatory columns (both always and conditional)
    always_mandatory = list(config['always_mandatory'])
    conditional_mandatory = []
    
    # Collect all conditional mandatory columns
    for rule in config.get('conditional_mandatory', []):
        conditional_mandatory.extend(rule['required_columns'])
    
    # Remove duplicates while preserving order
    conditional_mandatory = list(dict.fromkeys(conditional_mandatory))
    
    # Initialize missing columns DataFrame with only mandatory columns
    missing_always = pd.DataFrame(False, index=df.index, columns=always_mandatory)
    
    # Check always mandatory columns
    for col in always_mandatory:
        missing_always[col] = check_column_validity(df, col)
    
    # Check conditional mandatory columns
    missing_conditional = check_conditional_mandatory(df, config)
    
    # Combine missing columns
    missing_cols = pd.concat([missing_always, missing_conditional], axis=1)
    missing_cols = missing_cols.loc[:, ~missing_cols.columns.duplicated()]
    
    # Find rows with any missing mandatory columns
    has_missing = missing_cols.any(axis=1)
    
    # Split data while preserving all columns
    missing_data = df[has_missing].copy()
    complete_data = df[~has_missing].copy()
    
    # Add prediction columns for missing data
    if not missing_data.empty:
        missing_data['prediction'] = 'TRUE'
        missing_data['score'] = 100
        missing_data['key_drivers'] = missing_cols[has_missing].apply(
            lambda x: ' | '.join([f"{col} | 1.0" for col in x[x].index]),
            axis=1
        )
    
    return missing_data, complete_data


def prepare_features(data: pd.DataFrame, target_column: str, feature_encoders: Dict[str, Any], training: bool = False) -> pd.DataFrame:
    """
    Prepare features for modeling
    
    Args:
        data: Input DataFrame
        target_column: Name of the target column
        feature_encoders: Dictionary of feature encoders
        training: Whether this is for training (True) or inference (False)
    
    Returns:
        DataFrame with processed features
    """
    # Create a copy to avoid modifying the original
    processed = data.copy()
    
    # Handle categorical features
    categorical_columns = processed.select_dtypes(include=['object', 'category']).columns
    
    for col in categorical_columns:
        if col == target_column:
            continue
            
        if training:
            encoder = LabelEncoder()
            processed[col] = encoder.fit_transform(processed[col].fillna('missing'))
            feature_encoders[col] = encoder
        else:
            if col in feature_encoders:
                # Handle categories not seen during training
                encoder = feature_encoders[col]
                processed[col] = processed[col].fillna('missing')
                unseen = ~processed[col].isin(encoder.classes_)
                if unseen.any():
                    processed.loc[unseen, col] = 'missing'
                processed[col] = encoder.transform(processed[col])
            else:
                # If we don't have an encoder for this column, drop it
                processed.drop(columns=[col], inplace=True)
    
    # Fill numeric missing values with mean
    numeric_columns = processed.select_dtypes(include=['number']).columns
    for col in numeric_columns:
        if training:
            mean_val = processed[col].mean()
            processed[col] = processed[col].fillna(mean_val)
            # Store the mean for later use
            feature_encoders[f"{col}_mean"] = mean_val
        else:
            if f"{col}_mean" in feature_encoders:
                processed[col] = processed[col].fillna(feature_encoders[f"{col}_mean"])
    
    return processed


def train_ensemble_model(data: pd.DataFrame, target_column: str, model_dir: str,
                        categorical_features: Optional[List[str]] = None,
                        time_limit: int = 3600) -> Tuple[TabularPredictor, cb.CatBoostClassifier, Dict[str, Any]]:
    """
    Train the ensemble model (AutoGluon and CatBoost)
    
    Args:
        data: Training data
        target_column: Name of the target column
        model_dir: Directory to save models
        categorical_features: List of categorical feature names
        time_limit: Time limit for AutoGluon training in seconds
        
    Returns:
        Tuple of (AutoGluon model, CatBoost model, feature encoders)
    """
    feature_encoders = {}
    
    # Prepare features
    processed_data = prepare_features(data, target_column, feature_encoders, training=True)
    
    # Train AutoGluon model
    autogluon_dir = os.path.join(model_dir, 'autogluon')
    autogluon_model = TabularPredictor(
        label=target_column,
        path=autogluon_dir
    ).fit(
        processed_data,
        time_limit=time_limit,
        presets='best_quality'
    )
    
    # Train CatBoost model
    catboost_dir = os.path.join(model_dir, 'catboost')
    os.makedirs(catboost_dir, exist_ok=True)
    
    # Prepare CatBoost data
    X = processed_data.drop(columns=[target_column])
    y = processed_data[target_column]
    
    # Initialize and train CatBoost
    catboost_model = cb.CatBoostClassifier(
        iterations=1000,
        learning_rate=0.1,
        depth=6,
        loss_function='Logloss',
        eval_metric='AUC',
        random_seed=42,
        verbose=100
    )
    
    catboost_model.fit(
        X, y,
        cat_features=categorical_features if categorical_features else [],
        eval_set=(X, y),
        use_best_model=True,
        plot=False
    )
    
    # Save CatBoost model
    catboost_model.save_model(os.path.join(catboost_dir, 'model.cbm'))
    
    # Save feature encoders
    joblib.dump(feature_encoders, os.path.join(model_dir, 'feature_encoders.joblib'))
    
    logger.info("Ensemble model training completed")
    
    return autogluon_model, catboost_model, feature_encoders


def predict_with_ensemble(data: pd.DataFrame, target_column: str,
                         autogluon_model: TabularPredictor,
                         catboost_model: cb.CatBoostClassifier,
                         feature_encoders: Dict[str, Any]) -> pd.DataFrame:
    """
    Make predictions using the ensemble model
    
    Args:
        data: Input DataFrame
        target_column: Name of the target column
        autogluon_model: Trained AutoGluon model
        catboost_model: Trained CatBoost model
        feature_encoders: Dictionary of feature encoders
        
    Returns:
        DataFrame with predictions, scores, and key drivers
    """
    # Prepare features
    processed_data = prepare_features(data, target_column, feature_encoders, training=False)
    
    # Get predictions from both models
    autogluon_preds = autogluon_model.predict_proba(processed_data)
    catboost_preds = catboost_model.predict_proba(processed_data)
    
    # Average the probabilities
    avg_probs = (autogluon_preds + catboost_preds) / 2
    
    # Convert to predictions and scores
    predictions = (avg_probs[:, 1] > 0.5).astype(str)
    predictions = np.where(predictions == 'True', 'TRUE', 'FALSE')
    
    # Convert probabilities to scores (0-100)
    scores = np.round(avg_probs[:, 1] * 100).astype(int)
    
    # Get feature importance for key drivers
    feature_importance = catboost_model.get_feature_importance()
    top_features = np.argsort(feature_importance)[-3:]  # Top 3 features
    
    # Create key drivers string
    key_drivers = []
    for idx in range(len(data)):
        driver_str = ' | '.join([
            f"{processed_data.columns[i]} | {feature_importance[i]:.1f}"
            for i in top_features
        ])
        key_drivers.append(driver_str)
    
    # Create result DataFrame
    result = data.copy()
    result['prediction'] = predictions
    result['score'] = scores
    result['key_drivers'] = key_drivers
    
    return result


def train_model(data: pd.DataFrame, target_column: str, config_path: str,
                model_dir: str, categorical_features: Optional[List[str]] = None,
                time_limit: int = 3600) -> Tuple[TabularPredictor, cb.CatBoostClassifier, Dict[str, Any]]:
    """
    Train the two-layer classification model
    
    Args:
        data: Training data
        target_column: Name of the target column
        config_path: Path to the configuration file
        model_dir: Directory to save models
        categorical_features: List of categorical feature names
        time_limit: Time limit for AutoGluon training in seconds
        
    Returns:
        Tuple of (AutoGluon model, CatBoost model, feature encoders)
    """
    # Filter data using business rules
    missing_data, complete_data = process_business_rules(data, config_path)
    
    if complete_data.empty:
        logger.warning("No data available for training after business rules filtering")
        return None, None, {}
    
    # Train ensemble model
    return train_ensemble_model(complete_data, target_column, model_dir,
                              categorical_features, time_limit)


def make_predictions(data: pd.DataFrame, target_column: str, config_path: str,
                    autogluon_model: TabularPredictor,
                    catboost_model: cb.CatBoostClassifier,
                    feature_encoders: Dict[str, Any]) -> pd.DataFrame:
    """
    Make predictions using both layers
    
    Args:
        data: Input DataFrame
        target_column: Name of the target column
        config_path: Path to the configuration file
        autogluon_model: Trained AutoGluon model
        catboost_model: Trained CatBoost model
        feature_encoders: Dictionary of feature encoders
        
    Returns:
        DataFrame with predictions, scores, and key drivers
    """
    # Process through business rules
    missing_data, complete_data = process_business_rules(data, config_path)
    
    # Process complete data through ensemble model
    if not complete_data.empty:
        complete_data = predict_with_ensemble(complete_data, target_column,
                                            autogluon_model, catboost_model,
                                            feature_encoders)
    
    # Combine results
    result = pd.concat([missing_data, complete_data], ignore_index=True)
    
    return result 
