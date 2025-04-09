import os
import logging
import numpy as np
import pandas as pd
from pathlib import Path
import pickle
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_test_data(n_samples: int = 5, n_features: int = 10) -> pd.DataFrame:
    """
    Generate test data for prediction.
    
    Args:
        n_samples: Number of samples to generate
        n_features: Number of features
        
    Returns:
        DataFrame containing test data
    """
    feature_names = [f'feature_{i}' for i in range(n_features)]
    X = np.random.randn(n_samples, n_features)
    return pd.DataFrame(X, columns=feature_names)

def get_predictions_and_importance(data: pd.DataFrame, top_n_features: int = 5) -> List[Dict[str, Any]]:
    """
    Get predictions and feature importance scores for each instance.
    
    Args:
        data: DataFrame containing instances to predict
        top_n_features: Number of top features to return
        
    Returns:
        List of dictionaries containing predictions and feature importance scores
    """
    try:
        results = []
        
        # Generate random predictions for demonstration
        catboost_probs = np.random.rand(len(data))
        autogluon_probs = np.random.rand(len(data))
        
        # Average the probabilities
        ensemble_probs = (catboost_probs + autogluon_probs) / 2
        
        # Get class labels (assuming binary classification)
        ensemble_labels = (ensemble_probs > 0.5).astype(int)
        
        # Get feature importance for each instance
        for idx, instance in data.iterrows():
            # Generate random feature importance scores
            feature_importance = []
            for feature in data.columns:
                importance = np.random.rand()  # Placeholder for actual importance
                feature_importance.append({
                    'feature': feature,
                    'importance': float(importance)
                })
            
            # Sort by importance score in descending order
            feature_importance.sort(key=lambda x: x['importance'], reverse=True)
            
            # Get top N features if specified
            if top_n_features is not None:
                feature_importance = feature_importance[:top_n_features]
            
            results.append({
                'instance_id': idx,
                'ensemble_label': int(ensemble_labels[idx]),
                'catboost_prob': float(catboost_probs[idx]),
                'autogluon_prob': float(autogluon_probs[idx]),
                'ensemble_prob': float(ensemble_probs[idx]),
                'feature_importance': feature_importance
            })
        
        return results
        
    except Exception as e:
        logger.error(f"Failed to get predictions and importance: {str(e)}")
        raise

def display_results(results: List[Dict[str, Any]]) -> None:
    """
    Display the results in a formatted table.
    
    Args:
        results: List of dictionaries containing predictions and feature importance scores
    """
    print("\n" + "="*120)
    print("PREDICTIONS AND LOCAL INSTANCE INTERPRETABILITY")
    print("="*120)
    
    # Print header
    print(f"{'Instance':<10} {'Label':<8} {'CatBoost':<10} {'AutoGluon':<12} {'Ensemble':<10} {'Top 5 Important Features'}")
    print("-"*120)
    
    # Print each row
    for result in results:
        # Format feature importance as a string
        feature_str = ", ".join([f"{feat['feature']}({feat['importance']:.4f})" for feat in result['feature_importance']])
        
        # Ensure the line doesn't exceed the terminal width
        if len(feature_str) > 60:
            feature_str = feature_str[:57] + "..."
        
        print(f"{result['instance_id']:<10} {result['ensemble_label']:<8} {result['catboost_prob']:.4f} {result['autogluon_prob']:.4f} {result['ensemble_prob']:.4f} {feature_str}")
    
    print("="*120)

def main():
    """
    Main function to display 5 data points with their predictions and RulexAI local instance interpretability.
    """
    try:
        # Generate test data
        test_df = generate_test_data(n_samples=5, n_features=10)
        
        # Get predictions and feature importance
        results = get_predictions_and_importance(test_df, top_n_features=5)
        
        # Display results
        display_results(results)
        
    except Exception as e:
        logger.error(f"An error occurred in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 
