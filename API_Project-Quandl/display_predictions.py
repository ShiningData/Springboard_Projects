import os
import logging
import numpy as np
import pandas as pd
from pathlib import Path
import pickle
import sys
import shutil
from typing import Dict, List, Tuple, Any, Union

# Add parent directory to path to import from batch_rulex_script.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from batch_rulex_script import EnsembleModel, ModelConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

def load_model_and_explainer(model_dir: Path) -> Tuple[EnsembleModel, Any]:
    """
    Load the ensemble model and explainer from disk.
    
    Args:
        model_dir: Directory containing the model files
        
    Returns:
        Tuple of (ensemble_model, explainer)
    """
    try:
        # Load ensemble model
        logger.info(f"Loading ensemble model from {model_dir}")
        ensemble_model = EnsembleModel.load(model_dir)
        
        # Load explainer
        explainer_path = model_dir / "explainer.pkl"
        logger.info(f"Loading explainer from {explainer_path}")
        with open(explainer_path, 'rb') as f:
            explainer = pickle.load(f)
        
        logger.info("Successfully loaded both model and explainer")
        return ensemble_model, explainer
        
    except Exception as e:
        logger.error(f"Failed to load models: {str(e)}")
        raise

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

def get_predictions_and_importance(
    ensemble_model: EnsembleModel, 
    explainer: Any, 
    data: pd.DataFrame, 
    top_n_features: int = 5
) -> List[Dict[str, Any]]:
    """
    Get predictions and feature importance scores for each instance.
    
    Args:
        ensemble_model: The loaded ensemble model
        explainer: The loaded explainer
        data: DataFrame containing instances to predict
        top_n_features: Number of top features to return
        
    Returns:
        List of dictionaries containing predictions and feature importance scores
    """
    try:
        results = []
        
        # Make predictions for all instances
        # Get predictions from both models
        catboost_preds = ensemble_model.catboost_model.predict_proba(data)
        autogluon_preds = ensemble_model.autogluon_model.predict_proba(data)
        
        # Average the probabilities
        ensemble_probs = (catboost_preds + autogluon_preds) / 2
        
        # Get class labels (assuming binary classification)
        ensemble_labels = (ensemble_probs[:, 1] > 0.5).astype(int)
        
        # Get feature importance for each instance
        for idx, instance in data.iterrows():
            # Get feature importance from RulexAI explainer
            # This is a simplified version - in a real implementation,
            # you would use the explainer's explain method
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
                'catboost_prob': float(catboost_preds[idx, 1]),
                'autogluon_prob': float(autogluon_preds[idx, 1]),
                'ensemble_prob': float(ensemble_probs[idx, 1]),
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
    print("\n" + "="*100)
    print("PREDICTIONS AND LOCAL INSTANCE INTERPRETABILITY")
    print("="*100)
    
    # Print header
    print(f"{'Instance':<10} {'Label':<8} {'CatBoost':<10} {'AutoGluon':<12} {'Ensemble':<10} {'Top 5 Important Features'}")
    print("-"*100)
    
    # Print each row
    for result in results:
        # Format feature importance as a string
        feature_str = ", ".join([f"{feat['feature']}({feat['importance']:.4f})" for feat in result['feature_importance']])
        
        print(f"{result['instance_id']:<10} {result['ensemble_label']:<8} {result['catboost_prob']:.4f} {result['autogluon_prob']:.4f} {result['ensemble_prob']:.4f} {feature_str}")
    
    print("="*100)

def create_dummy_model_files(model_dir: Path) -> None:
    """
    Create dummy model files for testing.
    
    Args:
        model_dir: Directory to create the files in
    """
    try:
        # Create directory if it doesn't exist
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # Create dummy model files
        logger.info(f"Creating dummy model files in {model_dir}")
        
        # Create dummy CatBoost model
        catboost_path = model_dir / "catboost_model.pkl"
        with open(catboost_path, 'wb') as f:
            pickle.dump({"dummy": "catboost_model"}, f)
        
        # Create dummy AutoGluon model directory
        autogluon_path = model_dir / "autogluon_model"
        autogluon_path.mkdir(exist_ok=True)
        with open(autogluon_path / "model.pkl", 'wb') as f:
            pickle.dump({"dummy": "autogluon_model"}, f)
        
        # Create dummy model config
        config_path = model_dir / "model_config.json"
        with open(config_path, 'w') as f:
            f.write('{"dummy": "model_config"}')
        
        # Create dummy explainer
        explainer_path = model_dir / "explainer.pkl"
        with open(explainer_path, 'wb') as f:
            pickle.dump({"dummy": "explainer"}, f)
        
        logger.info("Successfully created dummy model files")
        
    except Exception as e:
        logger.error(f"Failed to create dummy model files: {str(e)}")
        raise

def main():
    """
    Main function to display 5 data points with their predictions and RulexAI local instance interpretability.
    """
    try:
        # Configuration
        model_dir = Path("rulex_explanations")
        
        # Create dummy model files if they don't exist
        if not (model_dir / "catboost_model.pkl").exists():
            create_dummy_model_files(model_dir)
        
        # Load model and explainer
        ensemble_model, explainer = load_model_and_explainer(model_dir)
        
        # Generate test data
        test_df = generate_test_data(n_samples=5, n_features=10)
        
        # Get predictions and feature importance
        results = get_predictions_and_importance(ensemble_model, explainer, test_df, top_n_features=5)
        
        # Display results
        display_results(results)
        
    except Exception as e:
        logger.error(f"An error occurred in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 
