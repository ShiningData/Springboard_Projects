"""
Two-Layer Classification System

This system implements a classification pipeline with two layers:
1. Business Rules Layer: Checks for mandatory columns and handles missing data
2. Ensemble Model Layer: Combines AutoGluon and CatBoost predictions

The system maintains the original data and appends prediction, score, and key drivers columns.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional, Union, Set
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


def create_config_file(config_path: str, mandatory_columns: List[str]) -> None:
    """
    Create the mandatory columns configuration file
    
    Args:
        config_path: Path to save the configuration file
        mandatory_columns: List of mandatory column names
    """
    config = {
        'always_mandatory': mandatory_columns,
        'conditional_mandatory': []
    }
    
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)


class BusinessRulesLayer:
    """
    First layer of the classification system that handles business rules
    and checks for mandatory columns.
    """
    
    def __init__(self, config_path: str):
        """
        Initialize the business rules layer
        
        Args:
            config_path: Path to the mandatory columns configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load the mandatory columns configuration"""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _is_valid_value(self, value: Any) -> bool:
        """
        Check if a value is valid (not missing, empty, or whitespace)
        
        Args:
            value: The value to check
            
        Returns:
            bool: True if the value is valid, False otherwise
        """
        if pd.isna(value):
            return False
        
        if isinstance(value, str):
            # Check for empty strings or strings containing only whitespace
            return bool(value.strip())
        
        return True
    
    def _check_column_validity(self, df: pd.DataFrame, column: str) -> pd.Series:
        """
        Check if a column has valid values
        
        Args:
            df: Input DataFrame
            column: Column name to check
            
        Returns:
            Series of boolean values indicating invalid entries
        """
        # Check for invalid values
        return ~df[column].apply(self._is_valid_value)
    
    def _check_conditional_mandatory(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Check conditional mandatory columns based on state rules
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with missing mandatory columns marked
        """
        missing_cols = pd.DataFrame(False, index=df.index, columns=df.columns)
        
        # Check each conditional rule
        for rule in self.config.get('conditional_mandatory', []):
            condition_col = rule['condition']['column']
            condition_val = rule['condition']['value']
            required_cols = rule['required_columns']
            
            # Find rows matching the condition
            condition_mask = df[condition_col] == condition_val
            
            # Check required columns for matching rows
            for col in required_cols:
                invalid_mask = self._check_column_validity(df, col)
                missing_cols.loc[condition_mask, col] = invalid_mask[condition_mask]
        
        return missing_cols
    
    def process(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Process the input data through business rules
        
        Args:
            df: Input DataFrame
            
        Returns:
            Tuple of (DataFrame with missing mandatory columns, DataFrame with complete data)
        """
        # Check always mandatory columns
        always_mandatory = self.config['always_mandatory']
        missing_always = pd.DataFrame(False, index=df.index, columns=always_mandatory)
        
        for col in always_mandatory:
            missing_always[col] = self._check_column_validity(df, col)
        
        # Check conditional mandatory columns
        missing_conditional = self._check_conditional_mandatory(df)
        
        # Combine missing columns
        missing_cols = pd.concat([missing_always, missing_conditional], axis=1)
        missing_cols = missing_cols.loc[:, ~missing_cols.columns.duplicated()]
        
        # Find rows with any missing mandatory columns
        has_missing = missing_cols.any(axis=1)
        
        # Split data
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


class EnsembleModelLayer:
    """
    Second layer of the classification system that combines AutoGluon and CatBoost models.
    """
    
    def __init__(self, target_column: str, model_dir: str = 'models'):
        """
        Initialize the EnsembleModelLayer
        
        Args:
            target_column: The column name for the target variable
            model_dir: Directory to save/load models
        """
        self.target_column = target_column
        self.model_dir = model_dir
        self.autogluon_model = None
        self.catboost_model = None
        self.feature_encoders = {}
        self.feature_importance = {}
        os.makedirs(model_dir, exist_ok=True)
    
    def _prepare_features(self, data: pd.DataFrame, training: bool = False) -> pd.DataFrame:
        """
        Prepare features for modeling
        
        Args:
            data: Input DataFrame
            training: Whether this is for training (True) or inference (False)
        
        Returns:
            DataFrame with processed features
        """
        # Create a copy to avoid modifying the original
        processed = data.copy()
        
        # Handle categorical features
        categorical_columns = processed.select_dtypes(include=['object', 'category']).columns
        
        for col in categorical_columns:
            if col == self.target_column:
                continue
                
            if training:
                encoder = LabelEncoder()
                processed[col] = encoder.fit_transform(processed[col].fillna('missing'))
                self.feature_encoders[col] = encoder
            else:
                if col in self.feature_encoders:
                    # Handle categories not seen during training
                    encoder = self.feature_encoders[col]
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
                self.feature_encoders[f"{col}_mean"] = mean_val
            else:
                if f"{col}_mean" in self.feature_encoders:
                    processed[col] = processed[col].fillna(self.feature_encoders[f"{col}_mean"])
        
        return processed
    
    def train(self, data: pd.DataFrame, categorical_features: Optional[List[str]] = None,
              time_limit: int = 3600) -> None:
        """
        Train the ensemble model (AutoGluon and CatBoost)
        
        Args:
            data: Training data
            categorical_features: List of categorical feature names
            time_limit: Time limit for AutoGluon training in seconds
        """
        # Prepare features
        processed_data = self._prepare_features(data, training=True)
        
        # Train AutoGluon model
        autogluon_dir = os.path.join(self.model_dir, 'autogluon')
        self.autogluon_model = TabularPredictor(
            label=self.target_column,
            path=autogluon_dir
        ).fit(
            processed_data,
            time_limit=time_limit,
            presets='best_quality'
        )
        
        # Train CatBoost model
        catboost_dir = os.path.join(self.model_dir, 'catboost')
        os.makedirs(catboost_dir, exist_ok=True)
        
        # Prepare CatBoost data
        X = processed_data.drop(columns=[self.target_column])
        y = processed_data[self.target_column]
        
        # Initialize and train CatBoost
        self.catboost_model = cb.CatBoostClassifier(
            iterations=1000,
            learning_rate=0.1,
            depth=6,
            loss_function='Logloss',
            eval_metric='AUC',
            random_seed=42,
            verbose=100
        )
        
        self.catboost_model.fit(
            X, y,
            cat_features=categorical_features if categorical_features else [],
            eval_set=(X, y),
            use_best_model=True,
            plot=False
        )
        
        # Save CatBoost model
        self.catboost_model.save_model(os.path.join(catboost_dir, 'model.cbm'))
        
        # Save feature encoders
        joblib.dump(self.feature_encoders, os.path.join(self.model_dir, 'feature_encoders.joblib'))
        
        logger.info("Ensemble model training completed")
    
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Make predictions using the ensemble model
        
        Args:
            data: Input DataFrame
        
        Returns:
            DataFrame with predictions, scores, and key drivers
        """
        if self.autogluon_model is None or self.catboost_model is None:
            raise ValueError("Models not trained. Call train() first.")
        
        # Prepare features
        processed_data = self._prepare_features(data, training=False)
        
        # Get predictions from both models
        autogluon_preds = self.autogluon_model.predict_proba(processed_data)
        catboost_preds = self.catboost_model.predict_proba(processed_data)
        
        # Average the probabilities
        avg_probs = (autogluon_preds + catboost_preds) / 2
        
        # Convert to predictions and scores
        predictions = (avg_probs[:, 1] > 0.5).astype(str)
        predictions = np.where(predictions == 'True', 'TRUE', 'FALSE')
        
        # Convert probabilities to scores (0-100)
        scores = np.round(avg_probs[:, 1] * 100).astype(int)
        
        # Get feature importance for key drivers
        feature_importance = self.catboost_model.get_feature_importance()
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


class TwoLayerClassification:
    """
    Main class that combines both layers of the classification system.
    """
    
    def __init__(self, target_column: str, config_path: str, model_dir: str):
        """
        Initialize the two-layer classification system
        
        Args:
            target_column: The column name for the target variable
            config_path: Path to the mandatory columns configuration file
            model_dir: Directory to save/load models
        """
        self.target_column = target_column
        self.business_rules = BusinessRulesLayer(config_path)
        self.ensemble_model = EnsembleModelLayer(
            target_column=target_column,
            model_dir=model_dir or os.path.join(project_root, 'app', 'models')
        )
    
    def train(self, data: pd.DataFrame, categorical_features: Optional[List[str]] = None,
              time_limit: int = 3600) -> None:
        """
        Train the model
        
        Args:
            data: Training data
            categorical_features: List of categorical feature names
            time_limit: Time limit for AutoGluon training in seconds
        """
        # Filter data using business rules layer
        missing_data, complete_data = self.business_rules.process(data)
        
        if complete_data.empty:
            logger.warning("No data available for training after business rules filtering")
            return
        
        # Train ensemble model
        self.ensemble_model.train(complete_data, categorical_features, time_limit)
    
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Make predictions using both layers
        
        Args:
            data: Input DataFrame
        
        Returns:
            DataFrame with predictions, scores, and key drivers
        """
        # Process through business rules layer
        missing_data, complete_data = self.business_rules.process(data)
        
        # Process complete data through ensemble model
        if not complete_data.empty:
            complete_data = self.ensemble_model.predict(complete_data)
        
        # Combine results
        result = pd.concat([missing_data, complete_data], ignore_index=True)
        
        return result 
