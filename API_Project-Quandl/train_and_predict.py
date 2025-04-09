import os
import logging
import numpy as np
import pandas as pd
from pathlib import Path
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from batch_rulex_script import EnsembleModel, ModelConfig
from local_interpretability import LocalInterpretabilityManager
from model_predictor import ModelPredictor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_large_dataset(n_samples: int = 10_000_000, n_features: int = 20) -> pd.DataFrame:
    """
    Generate a large synthetic dataset for demonstration.
    
    Args:
        n_samples: Number of samples to generate
        n_features: Number of features
        
    Returns:
        DataFrame containing the synthetic data
    """
    logger.info(f"Generating synthetic dataset with {n_samples} samples and {n_features} features")
    
    # Generate feature names
    feature_names = [f'feature_{i}' for i in range(n_features)]
    
    # Generate synthetic data
    # For demonstration, we'll use a smaller dataset
    # In a real scenario, you would load your actual data
    actual_samples = min(n_samples, 100_000)  # Limit to 100,000 for demonstration
    logger.info(f"Using {actual_samples} samples for demonstration")
    
    X = np.random.randn(actual_samples, n_features)
    df = pd.DataFrame(X, columns=feature_names)
    
    # Add a target column (binary classification)
    df['target'] = (np.random.rand(actual_samples) > 0.5).astype(int)
    
    return df

def train_ensemble_model(data: pd.DataFrame, model_dir: Path) -> None:
    """
    Train the ensemble model and save it.
    
    Args:
        data: DataFrame containing training data
        model_dir: Directory to save the model
    """
    logger.info("Training ensemble model")
    
    # Create model directory
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # Create model configuration
    feature_names = [col for col in data.columns if col != 'target']
    config = ModelConfig(
        target_column='target',
        categorical_features=[],
        numerical_features=feature_names
    )
    
    # Create and train the model
    model = EnsembleModel(config)
    model.fit(data)
    
    # Save the model
    model_path = model_dir / "ensemble_model"
    model.save(model_path)
    logger.info(f"Saved ensemble model to {model_path}")

def train_explainer(data: pd.DataFrame, model_dir: Path) -> None:
    """
    Train the RulexAI explainer and save it.
    
    Args:
        data: DataFrame containing training data
        model_dir: Directory containing the saved model
    """
    logger.info("Training RulexAI explainer")
    
    # Initialize the interpretability manager
    model_path = model_dir / "ensemble_model"
    cache_dir = model_dir / "rulexai_cache"
    interpretability_manager = LocalInterpretabilityManager(
        model_path=str(model_path),
        batch_size=10000,
        cache_dir=str(cache_dir)
    )
    
    # Train and save the explainer
    explainer_path = model_dir / "rulexai_explainer.pkl"
    interpretability_manager.train_and_save_explainer(
        data=data,
        save_path=str(explainer_path),
        sample_size=50000  # Use 50,000 samples for training
    )
    logger.info(f"Saved RulexAI explainer to {explainer_path}")

def predict_and_explain(model_dir: Path, n_samples: int = 5) -> None:
    """
    Make predictions and display interpretations for a few instances.
    
    Args:
        model_dir: Directory containing the saved model and explainer
        n_samples: Number of samples to predict and explain
    """
    logger.info(f"Making predictions and displaying interpretations for {n_samples} instances")
    
    # Generate test data
    n_features = 20
    feature_names = [f'feature_{i}' for i in range(n_features)]
    X = np.random.randn(n_samples, n_features)
    test_df = pd.DataFrame(X, columns=feature_names)
    
    # Initialize predictor
    model_path = model_dir / "ensemble_model"
    explainer_path = model_dir / "rulexai_explainer.pkl"
    predictor = ModelPredictor(model_path, explainer_path)
    
    # Load models
    predictor.load_models()
    
    # Make predictions with feature importance
    results = predictor.predict_with_importance(test_df, top_n_features=3)
    
    # Print results
    for result in results:
        print(f"\nInstance {result['instance_id']}:")
        print(f"Prediction: {result['prediction']:.4f}")
        print("Top 3 Important Features:")
        for feat in result['feature_importance']:
            print(f"  {feat['feature']}: {feat['importance']:.4f}")

def main():
    """
    Main function to demonstrate the workflow.
    """
    try:
        # Configuration
        model_dir = Path("rulex_explanations")
        
        # Generate large dataset
        data = generate_large_dataset(n_samples=10_000_000, n_features=20)
        
        # Train ensemble model
        train_ensemble_model(data, model_dir)
        
        # Train explainer
        train_explainer(data, model_dir)
        
        # Make predictions and display interpretations
        predict_and_explain(model_dir, n_samples=5)
        
        logger.info("Workflow completed successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 
