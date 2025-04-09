import os
import json
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Union, Any, Optional, Tuple
from pathlib import Path
import pickle
from tqdm import tqdm
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - INFO - %(message)s'
)
logger = logging.getLogger(__name__)

# Import RulexAI and RuleKit packages with detailed error handling
RULEXAI_AVAILABLE = False
try:
    logger.info("Attempting to import RulexAI and RuleKit packages...")
    from rulexai import RulexAIExplainer
    from rulekit import RuleKit
    RULEXAI_AVAILABLE = True
    logger.info("Successfully imported RulexAI and RuleKit packages")
except ImportError as e:
    logger.error(f"Failed to import RulexAI or RuleKit: {str(e)}")
    logger.error(f"Python path: {sys.path}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    logger.warning("RulexAI or RuleKit packages not available. Install with: pip install rulexai rulekit")

# Import functions from batch_rulex_script
try:
    from batch_rulex_script import (
        create_ensemble_model, 
        process_dataset, 
        save_explainer, 
        load_explainer,
        init_directories
    )
    logger.info("Successfully imported functions from batch_rulex_script")
except ImportError as e:
    logger.error(f"Failed to import functions from batch_rulex_script: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")

class LocalInterpretabilityManager:
    """
    Manages local interpretability for the ensemble model using RulexAI.
    Handles batch processing for large datasets and saves/loads explainers.
    """
    
    def __init__(
        self,
        model_path: str,
        batch_size: int = 10000,
        max_workers: int = 4,
        cache_dir: str = "rulexai_cache"
    ):
        """
        Initialize the local interpretability manager.
        
        Args:
            model_path: Path to the saved ensemble model
            batch_size: Number of instances to process in each batch
            max_workers: Maximum number of parallel workers for batch processing
            cache_dir: Directory to cache RulexAI explainers
        """
        self.model_path = model_path
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.cache_dir = cache_dir
        self.ensemble_model = None
        self.explainer = None
        self.feature_names = None
        
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        
        # Check if RulexAI is available
        if not RULEXAI_AVAILABLE:
            logger.error("RulexAI or RuleKit packages not available. Install with: pip install rulexai rulekit")
            raise ImportError("Required packages not available")
    
    def load_ensemble_model(self) -> None:
        """Load the ensemble model from disk."""
        logger.info(f"Loading ensemble model from {self.model_path}")
        with open(self.model_path, 'rb') as f:
            self.ensemble_model = pickle.load(f)
        self.feature_names = self.ensemble_model['feature_names']
        logger.info(f"Ensemble model loaded successfully with {len(self.feature_names)} features")
    
    def _process_batch(
        self, 
        batch_data: pd.DataFrame, 
        batch_id: int
    ) -> Tuple[int, Any]:
        """
        Process a single batch of data with RulexAI.
        
        Args:
            batch_data: DataFrame containing the batch of instances
            batch_id: Identifier for the batch
            
        Returns:
            Tuple of (batch_id, explainer)
        """
        logger.info(f"Processing batch {batch_id} with {len(batch_data)} instances")
        
        # Create a unique explainer for this batch
        explainer = RulexAIExplainer(
            model=self.ensemble_model,
            feature_names=self.feature_names,
            rulekit=RuleKit()
        )
        
        # Fit the explainer on this batch
        explainer.fit(batch_data)
        
        return batch_id, explainer
    
    def process_data_in_batches(
        self, 
        data: pd.DataFrame, 
        save_explainers: bool = True
    ) -> Dict[int, Any]:
        """
        Process data in batches and generate explainers.
        
        Args:
            data: DataFrame containing all instances
            save_explainers: Whether to save explainers to disk
            
        Returns:
            Dictionary mapping batch IDs to explainers
        """
        if self.ensemble_model is None:
            self.load_ensemble_model()
        
        # Split data into batches
        n_batches = (len(data) + self.batch_size - 1) // self.batch_size
        batches = [data.iloc[i:i+self.batch_size] for i in range(0, len(data), self.batch_size)]
        
        logger.info(f"Processing {len(data)} instances in {n_batches} batches")
        
        explainers = {}
        
        # Process batches in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_batch = {
                executor.submit(self._process_batch, batch, i): i 
                for i, batch in enumerate(batches)
            }
            
            for future in tqdm(as_completed(future_to_batch), total=len(batches), desc="Processing batches"):
                batch_id, explainer = future.result()
                explainers[batch_id] = explainer
                
                # Save explainer if requested
                if save_explainers:
                    self._save_explainer(explainer, batch_id)
        
        return explainers
    
    def _save_explainer(self, explainer: Any, batch_id: int) -> None:
        """Save an explainer to disk."""
        save_path = os.path.join(self.cache_dir, f"explainer_batch_{batch_id}.pkl")
        with open(save_path, 'wb') as f:
            pickle.dump(explainer, f)
        logger.info(f"Saved explainer for batch {batch_id} to {save_path}")
    
    def _load_explainer(self, batch_id: int) -> Any:
        """Load an explainer from disk."""
        load_path = os.path.join(self.cache_dir, f"explainer_batch_{batch_id}.pkl")
        if not os.path.exists(load_path):
            logger.warning(f"Explainer for batch {batch_id} not found at {load_path}")
            return None
        
        with open(load_path, 'rb') as f:
            explainer = pickle.load(f)
        logger.info(f"Loaded explainer for batch {batch_id} from {load_path}")
        return explainer
    
    def load_all_explainers(self) -> Dict[int, Any]:
        """Load all saved explainers from disk."""
        explainers = {}
        for filename in os.listdir(self.cache_dir):
            if filename.startswith("explainer_batch_") and filename.endswith(".pkl"):
                batch_id = int(filename.split("_")[2].split(".")[0])
                explainers[batch_id] = self._load_explainer(batch_id)
        
        logger.info(f"Loaded {len(explainers)} explainers from disk")
        return explainers
    
    def explain_instance(
        self, 
        instance: pd.DataFrame, 
        batch_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate explanation for a single instance.
        
        Args:
            instance: DataFrame containing a single instance
            batch_id: ID of the batch to use for explanation (if None, uses the first available)
            
        Returns:
            Dictionary containing the explanation
        """
        if self.ensemble_model is None:
            self.load_ensemble_model()
        
        # If no batch_id specified, use the first available explainer
        if batch_id is None:
            explainers = self.load_all_explainers()
            if not explainers:
                logger.warning("No explainers available. Processing instance directly.")
                explainer = RulexAIExplainer(
                    model=self.ensemble_model,
                    feature_names=self.feature_names,
                    rulekit=RuleKit()
                )
                explainer.fit(instance)
            else:
                batch_id = min(explainers.keys())
                explainer = explainers[batch_id]
        else:
            explainer = self._load_explainer(batch_id)
            if explainer is None:
                logger.warning(f"Explainer for batch {batch_id} not found. Processing instance directly.")
                explainer = RulexAIExplainer(
                    model=self.ensemble_model,
                    feature_names=self.feature_names,
                    rulekit=RuleKit()
                )
                explainer.fit(instance)
        
        # Generate explanation
        explanation = explainer.explain(instance)
        return explanation
    
    def explain_batch(
        self, 
        batch_data: pd.DataFrame, 
        batch_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate explanations for a batch of instances.
        
        Args:
            batch_data: DataFrame containing multiple instances
            batch_id: ID of the batch to use for explanation (if None, uses the first available)
            
        Returns:
            List of dictionaries containing explanations
        """
        explanations = []
        for _, instance in batch_data.iterrows():
            instance_df = pd.DataFrame([instance])
            explanation = self.explain_instance(instance_df, batch_id)
            explanations.append(explanation)
        
        return explanations

    def save_explainer(self, save_path: str) -> None:
        """
        Save the RulexAI explainer to disk.
        
        Args:
            save_path: Path to save the explainer
        """
        if self.explainer is None:
            raise ValueError("No explainer available to save. Call process_data_in_batches first.")
        
        try:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                pickle.dump(self.explainer, f)
            logger.info(f"Saved RulexAI explainer to {save_path}")
        except Exception as e:
            logger.error(f"Failed to save explainer: {str(e)}")
            raise

    def load_explainer(self, load_path: str) -> None:
        """
        Load a RulexAI explainer from disk.
        
        Args:
            load_path: Path to load the explainer from
        """
        try:
            if not os.path.exists(load_path):
                raise FileNotFoundError(f"Explainer file not found at {load_path}")
            
            with open(load_path, 'rb') as f:
                self.explainer = pickle.load(f)
            logger.info(f"Loaded RulexAI explainer from {load_path}")
        except Exception as e:
            logger.error(f"Failed to load explainer: {str(e)}")
            raise

    def get_feature_importance(self, instance: pd.DataFrame) -> List[Dict[str, float]]:
        """
        Get feature importance scores for a single instance.
        
        Args:
            instance: DataFrame containing a single instance
            
        Returns:
            List of dictionaries containing feature names and their importance scores
        """
        if self.explainer is None:
            raise ValueError("No explainer available. Call load_explainer first.")
        
        try:
            # Get explanation for the instance
            explanation = self.explainer.explain(instance)
            
            # Extract feature importance scores
            feature_importance = []
            for feature, score in explanation.get('feature_importance', {}).items():
                feature_importance.append({
                    'feature': feature,
                    'importance': float(score)
                })
            
            # Sort by importance score in descending order
            feature_importance.sort(key=lambda x: x['importance'], reverse=True)
            
            return feature_importance
        except Exception as e:
            logger.error(f"Failed to get feature importance: {str(e)}")
            raise

    def train_and_save_explainer(
        self, 
        data: pd.DataFrame, 
        save_path: str,
        sample_size: int = 100000
    ) -> None:
        """
        Train a RulexAI explainer on a sample of the data and save it.
        
        Args:
            data: DataFrame containing all instances
            save_path: Path to save the final explainer
            sample_size: Number of instances to use for training (default: 100,000)
        """
        try:
            logger.info(f"Training explainer on {sample_size} instances from {len(data)} total instances")
            
            # Sample data if it's larger than sample_size
            if len(data) > sample_size:
                sample_data = data.sample(n=sample_size, random_state=42)
                logger.info(f"Sampled {sample_size} instances for training")
            else:
                sample_data = data
                logger.info(f"Using all {len(data)} instances for training")
            
            # Process the sample data in batches
            explainers = self.process_data_in_batches(sample_data, save_explainers=True)
            
            # Combine explainers into a single explainer
            # This is a simplified approach - in a real implementation, you might want to
            # use a more sophisticated method to combine explainers
            logger.info("Combining batch explainers into a single explainer")
            
            # For simplicity, we'll use the explainer from the first batch
            # In a production environment, you might want to implement a more sophisticated
            # method to combine explainers from different batches
            self.explainer = explainers[min(explainers.keys())]
            
            # Save the final explainer
            self.save_explainer(save_path)
            logger.info(f"Saved final explainer to {save_path}")
            
        except Exception as e:
            logger.error(f"Failed to train and save explainer: {str(e)}")
            raise

def main():
    """
    Main function to demonstrate the local interpretability workflow.
    """
    try:
        # Configuration
        model_dir = "rulex_explanations"
        model_path = os.path.join(model_dir, "ensemble_model.pkl")
        cache_dir = "rulexai_cache"
        batch_size = 10000
        
        # Initialize the interpretability manager
        interpretability_manager = LocalInterpretabilityManager(
            model_path=model_path,
            batch_size=batch_size,
            cache_dir=cache_dir
        )
        
        # Load the ensemble model
        interpretability_manager.load_ensemble_model()
        
        # Generate synthetic data for demonstration
        # In a real scenario, you would load your 10 million records here
        logger.info("Generating synthetic data for demonstration...")
        n_samples = 100000  # For demonstration, use a smaller dataset
        n_features = len(interpretability_manager.feature_names)
        
        # Create synthetic data
        X = np.random.randn(n_samples, n_features)
        df = pd.DataFrame(X, columns=interpretability_manager.feature_names)
        
        # Train and save the explainer
        explainer_path = os.path.join(model_dir, "rulexai_explainer.pkl")
        interpretability_manager.train_and_save_explainer(df, explainer_path, sample_size=50000)
        
        logger.info("Local interpretability demonstration completed successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred in main: {str(e)}")
        raise


if __name__ == "__main__":
    main()
