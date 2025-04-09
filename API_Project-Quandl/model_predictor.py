import os
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Union, Any, Optional
from pathlib import Path
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from batch_rulex_script import EnsembleModel, ModelConfig
from local_interpretability import LocalInterpretabilityManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

class ModelPredictor:
    """
    Handles loading models and explainers, making predictions, and getting feature importance scores.
    """
    
    def __init__(
        self,
        model_path: Union[str, Path],
        explainer_path: Union[str, Path]
    ):
        """
        Initialize the model predictor.
        
        Args:
            model_path: Path to the saved ensemble model
            explainer_path: Path to the saved RulexAI explainer
        """
        self.model_path = Path(model_path)
        self.explainer_path = Path(explainer_path)
        self.model = None
        self.interpretability_manager = None
        
        # Validate paths
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model path does not exist: {self.model_path}")
        if not self.explainer_path.exists():
            raise FileNotFoundError(f"Explainer path does not exist: {self.explainer_path}")
    
    def load_models(self) -> None:
        """Load both the ensemble model and RulexAI explainer."""
        try:
            # Load ensemble model
            logger.info(f"Loading ensemble model from {self.model_path}")
            self.model = EnsembleModel(ModelConfig(
                target_column='target',  # This will be updated from saved config
                categorical_features=[],
                numerical_features=[]  # This will be updated from saved config
            ))
            self.model.load(self.model_path)
            
            # Load interpretability manager and explainer
            logger.info(f"Loading RulexAI explainer from {self.explainer_path}")
            self.interpretability_manager = LocalInterpretabilityManager(
                model_path=str(self.model_path),
                cache_dir=str(self.explainer_path.parent)
            )
            self.interpretability_manager.load_explainer(str(self.explainer_path))
            
            logger.info("Successfully loaded both models")
            
        except Exception as e:
            logger.error(f"Failed to load models: {str(e)}")
            raise
    
    def predict_with_importance(
        self,
        data: pd.DataFrame,
        top_n_features: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Make predictions and get feature importance scores for each instance.
        
        Args:
            data: DataFrame containing instances to predict
            top_n_features: Number of top features to return (if None, return all)
            
        Returns:
            List of dictionaries containing predictions and feature importance scores
        """
        if self.model is None or self.interpretability_manager is None:
            raise ValueError("Models not loaded. Call load_models() first.")
        
        try:
            results = []
            
            # Make predictions for all instances
            predictions = self.model.predict(data)
            
            # Get feature importance for each instance
            for idx, instance in data.iterrows():
                instance_df = pd.DataFrame([instance])
                feature_importance = self.interpretability_manager.get_feature_importance(instance_df)
                
                # Get top N features if specified
                if top_n_features is not None:
                    feature_importance = feature_importance[:top_n_features]
                
                results.append({
                    'instance_id': idx,
                    'prediction': float(predictions[idx]),
                    'feature_importance': feature_importance
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to make predictions: {str(e)}")
            raise

def main():
    """
    Example usage of the ModelPredictor class.
    """
    try:
        # Configuration
        model_dir = Path("rulex_explanations")
        model_path = model_dir / "ensemble_model"
        explainer_path = model_dir / "rulexai_explainer.pkl"
        
        # Initialize predictor
        predictor = ModelPredictor(model_path, explainer_path)
        
        # Load models
        predictor.load_models()
        
        # Generate example data
        n_samples = 5
        n_features = 10
        feature_names = [f'feature_{i}' for i in range(n_features)]
        
        X = np.random.randn(n_samples, n_features)
        test_df = pd.DataFrame(X, columns=feature_names)
        
        # Make predictions with feature importance
        results = predictor.predict_with_importance(test_df, top_n_features=3)
        
        # Print results
        for result in results:
            print(f"\nInstance {result['instance_id']}:")
            print(f"Prediction: {result['prediction']:.4f}")
            print("Top 3 Important Features:")
            for feat in result['feature_importance']:
                print(f"  {feat['feature']}: {feat['importance']:.4f}")
        
    except Exception as e:
        logger.error(f"An error occurred in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 
