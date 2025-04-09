import os
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Union, Any, Optional
from pathlib import Path
import pickle

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

class SimplePredictor:
    """
    A simplified predictor that loads a model and explainer, makes predictions,
    and gets feature importance scores.
    """
    
    def __init__(
        self,
        model_path: Union[str, Path],
        explainer_path: Union[str, Path]
    ):
        """
        Initialize the predictor.
        
        Args:
            model_path: Path to the saved model
            explainer_path: Path to the saved explainer
        """
        self.model_path = Path(model_path)
        self.explainer_path = Path(explainer_path)
        self.model = None
        self.explainer = None
        
        # Validate paths
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model path does not exist: {self.model_path}")
        if not self.explainer_path.exists():
            raise FileNotFoundError(f"Explainer path does not exist: {self.explainer_path}")
    
    def load_models(self) -> None:
        """Load both the model and explainer."""
        try:
            # Load model
            logger.info(f"Loading model from {self.model_path}")
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            # Load explainer
            logger.info(f"Loading explainer from {self.explainer_path}")
            with open(self.explainer_path, 'rb') as f:
                self.explainer = pickle.load(f)
            
            logger.info("Successfully loaded both model and explainer")
            
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
        if self.model is None or self.explainer is None:
            raise ValueError("Models not loaded. Call load_models() first.")
        
        try:
            results = []
            
            # Make predictions for all instances
            # This is a simplified version - in a real implementation,
            # you would use the model's predict method
            predictions = np.random.rand(len(data))  # Placeholder for actual predictions
            
            # Get feature importance for each instance
            for idx, instance in data.iterrows():
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
                    'prediction': float(predictions[idx]),
                    'feature_importance': feature_importance
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to make predictions: {str(e)}")
            raise

def main():
    """
    Example usage of the SimplePredictor class.
    """
    try:
        # Configuration
        model_dir = Path("rulex_explanations")
        model_path = model_dir / "model.pkl"
        explainer_path = model_dir / "explainer.pkl"
        
        # Create model and explainer files if they don't exist
        if not model_path.exists():
            logger.info(f"Creating dummy model file at {model_path}")
            model_dir.mkdir(parents=True, exist_ok=True)
            with open(model_path, 'wb') as f:
                pickle.dump({"dummy": "model"}, f)
        
        if not explainer_path.exists():
            logger.info(f"Creating dummy explainer file at {explainer_path}")
            with open(explainer_path, 'wb') as f:
                pickle.dump({"dummy": "explainer"}, f)
        
        # Initialize predictor
        predictor = SimplePredictor(model_path, explainer_path)
        
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
