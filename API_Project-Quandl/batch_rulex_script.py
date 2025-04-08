    # Save the ensemble model
    logger.info("Saving the trained ensemble model...")
    ensemble_path = os.path.join("rulex_explanations", "ensemble_model.pkl")
    with open(ensemble_path, 'wb') as f:
        pickle.dump(model, f)
    logger.info(f"Ensemble#!/usr/bin/env python
# Batch Processing with RulexAI for Large-Scale Model Interpretability

import os
import pandas as pd
import numpy as np
import pickle
import time
from datetime import datetime
import logging
from tqdm import tqdm
import rulex  # The RulexAI package
from joblib import Parallel, delayed, parallel_backend
import multiprocessing
from sklearn.ensemble import RandomForestClassifier
import shutil

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("rulex_batch_processing.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("RulexBatchProcessor")

class RulexBatchProcessor:
    """
    Class to handle batch processing of model explanations using RulexAI
    for a very large dataset (10M records)
    """
    
    def __init__(
        self, 
        model, 
        X_train, 
        feature_names, 
        output_dir="rulex_explanations",
        batch_size=10000, 
        n_jobs=-1,
        checkpoint_frequency=10,
        saved_explainer_path=None
    ):
        """
        Initialize the batch processor
        
        Args:
            model: The trained ensemble model to explain
            X_train: Training data used for the model
            feature_names: List of feature names
            output_dir: Directory to store explanations
            batch_size: Number of records to process in each batch
            n_jobs: Number of parallel jobs (-1 for all cores)
            checkpoint_frequency: How often to save checkpoints (in batches)
            saved_explainer_path: Path to a saved RulexAI explainer object (if available)
        """
        self.model = model
        self.X_train = X_train
        self.feature_names = feature_names
        self.output_dir = output_dir
        self.batch_size = batch_size
        self.n_jobs = n_jobs if n_jobs > 0 else multiprocessing.cpu_count()
        self.checkpoint_frequency = checkpoint_frequency
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(f"{output_dir}/checkpoints", exist_ok=True)
        os.makedirs(f"{output_dir}/explainer", exist_ok=True)
        
        # Load or initialize RulexAI explainer
        if saved_explainer_path and os.path.exists(saved_explainer_path):
            logger.info(f"Loading saved RulexAI explainer from {saved_explainer_path}")
            self.explainer = self.load_explainer(saved_explainer_path)
        else:
            logger.info("Initializing new RulexAI explainer...")
            # Set explicitly to use CPU only
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU
            self.explainer = rulex.RulexExplainer(
                model, 
                X_train, 
                feature_names=feature_names
            )
            # Save the explainer for future use
            self.save_explainer()
        
        logger.info(f"Processor initialized with batch size: {batch_size}, cores: {self.n_jobs}")
        
    def _save_checkpoint(self, batch_results, batch_num):
        """Save checkpoint of batch results"""
        checkpoint_path = f"{self.output_dir}/checkpoints/batch_{batch_num}.pkl"
        with open(checkpoint_path, 'wb') as f:
            pickle.dump(batch_results, f)
        logger.info(f"Checkpoint saved: {checkpoint_path}")
        
    def _process_single_record(self, idx, X_record):
        """Process a single record and return its explanation"""
        try:
            # Generate explanation for this record
            explanation = self.explainer.explain_instance(X_record)
            return idx, explanation
        except Exception as e:
            logger.error(f"Error processing record {idx}: {str(e)}")
            return idx, None
        
    def _process_batch(self, batch_indices, X_batch, batch_num):
        """Process a batch of records in parallel"""
        logger.info(f"Processing batch {batch_num}: {len(batch_indices)} records")
        start_time = time.time()
        
        results = []
        with parallel_backend('loky', n_jobs=self.n_jobs):
            results = Parallel(verbose=1)(
                delayed(self._process_single_record)(idx, X_batch[i]) 
                for i, idx in enumerate(batch_indices)
            )
            
        # Filter out failed explanations
        valid_results = [(idx, exp) for idx, exp in results if exp is not None]
        
        elapsed = time.time() - start_time
        logger.info(f"Batch {batch_num} processed in {elapsed:.2f}s " +
                    f"({len(valid_results)}/{len(batch_indices)} successful)")
        
        # Save checkpoint if needed
        if batch_num % self.checkpoint_frequency == 0:
            self._save_checkpoint(valid_results, batch_num)
            
        return valid_results
    
    def process_dataset(self, X_to_explain, starting_batch=0, resume_from_checkpoint=None, 
                       save_explainer_frequency=20):
        """
        Process the entire dataset in batches
        
        Args:
            X_to_explain: The dataset to generate explanations for
            starting_batch: Batch number to start processing from
            resume_from_checkpoint: Path to checkpoint to resume from
            save_explainer_frequency: How often to save the explainer (in batches)
                                     to capture any updates during processing
        """
        total_records = len(X_to_explain)
        total_batches = (total_records + self.batch_size - 1) // self.batch_size
        
        logger.info(f"Starting batch processing of {total_records} records " +
                   f"in {total_batches} batches (CPU-only mode)")
        
        all_explanations = {}
        
        # Resume from checkpoint if specified
        if resume_from_checkpoint and os.path.exists(resume_from_checkpoint):
            logger.info(f"Resuming from checkpoint: {resume_from_checkpoint}")
            with open(resume_from_checkpoint, 'rb') as f:
                checkpoint_results = pickle.load(f)
                for idx, exp in checkpoint_results:
                    all_explanations[idx] = exp
        
        # Process batches
        for batch_num in range(starting_batch, total_batches):
            start_idx = batch_num * self.batch_size
            end_idx = min(start_idx + self.batch_size, total_records)
            
            batch_indices = list(range(start_idx, end_idx))
            X_batch = X_to_explain[start_idx:end_idx]
            
            # Process this batch
            batch_results = self._process_batch(batch_indices, X_batch, batch_num)
            
            # Add to overall results
            for idx, exp in batch_results:
                all_explanations[idx] = exp
                
            # Save progress report
            completion_percentage = (batch_num + 1) / total_batches * 100
            logger.info(f"Progress: {completion_percentage:.2f}% complete " +
                       f"({batch_num + 1}/{total_batches} batches)")
            
            # Periodically save the explainer object to capture any learning/updates
            if batch_num % save_explainer_frequency == 0:
                explainer_path = self.save_explainer(f"rulex_explainer_batch_{batch_num}.pkl")
                logger.info(f"Saved explainer snapshot at batch {batch_num}: {explainer_path}")
            
        logger.info(f"Batch processing complete. Successful explanations: {len(all_explanations)}")
        return all_explanations
    
    def save_explainer(self, filename="rulex_explainer.pkl"):
        """Save the RulexAI explainer object to disk"""
        filepath = os.path.join(self.output_dir, "explainer", filename)
        with open(filepath, 'wb') as f:
            pickle.dump(self.explainer, f)
        logger.info(f"RulexAI explainer saved to: {filepath}")
        return filepath
    
    def load_explainer(self, filepath):
        """Load a RulexAI explainer object from disk"""
        with open(filepath, 'rb') as f:
            explainer = pickle.load(f)
        logger.info(f"RulexAI explainer loaded from: {filepath}")
        return explainer
        
    def save_explanations(self, explanations, filename="explanations.pkl"):
        """Save all explanations to disk"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'wb') as f:
            pickle.dump(explanations, f)
        logger.info(f"Explanations saved to: {filepath}")
        return filepath
    
    def generate_summary_report(self, explanations):
        """Generate a summary report of the explanations"""
        # Here you would implement logic to analyze all explanations
        # and create aggregated insights
        # ...
        
        # Save summary to file
        report_path = f"{self.output_dir}/summary_report.txt"
        with open(report_path, 'w') as f:
            f.write(f"RulexAI Explanation Summary\n")
            f.write(f"Generated on: {datetime.now()}\n")
            f.write(f"Total Records Processed: {len(explanations)}\n")
            # Add more summary statistics here
        
        logger.info(f"Summary report generated: {report_path}")
        return report_path


# Command-line interface for the batch processor
def parse_arguments():
    """Parse command line arguments"""
    import argparse
    parser = argparse.ArgumentParser(description='Batch process model explanations using RulexAI')
    
    parser.add_argument('--model_path', type=str, required=True,
                        help='Path to the saved ensemble model')
    parser.add_argument('--data_path', type=str, required=True,
                        help='Path to the dataset to explain')
    parser.add_argument('--train_data_path', type=str, required=True,
                        help='Path to the training data used for the model')
    parser.add_argument('--output_dir', type=str, default='rulex_explanations',
                        help='Directory to store explanations')
    parser.add_argument('--batch_size', type=int, default=50000,
                        help='Number of records to process in each batch')
    parser.add_argument('--n_jobs', type=int, default=8,
                        help='Number of parallel jobs')
    parser.add_argument('--checkpoint_freq', type=int, default=5,
                        help='How often to save checkpoints (in batches)')
    parser.add_argument('--resume', action='store_true',
                        help='Resume from the latest checkpoint')
    parser.add_argument('--explainer_path', type=str,
                        help='Path to a saved RulexAI explainer')
    
    return parser.parse_args()

# Example usage
if __name__ == "__main__":
    # This section can be used for both demonstration and actual CLI usage
    
    # Check if running in demo mode or CLI mode
    import sys
    if len(sys.argv) > 1:
        # CLI mode - parse arguments
        args = parse_arguments()
        
        logger.info("Loading model and dataset from specified paths...")
        # Load the model from the specified path
        with open(args.model_path, 'rb') as f:
            model = pickle.load(f)
            
        # Load the data (this should be adjusted based on your data format)
        X_all = pd.read_csv(args.data_path).values
        X_train = pd.read_csv(args.train_data_path).values
        
        # Get feature names from the training data
        if args.train_data_path.endswith('.csv'):
            feature_names = list(pd.read_csv(args.train_data_path).columns)
        else:
            # Default feature names if not available
            feature_names = [f"feature_{i}" for i in range(X_train.shape[1])]
        
        # Determine if we should resume from a checkpoint
        if args.resume:
            checkpoint_dir = os.path.join(args.output_dir, "checkpoints")
            checkpoints = [f for f in os.listdir(checkpoint_dir) if f.startswith("batch_") and f.endswith(".pkl")] if os.path.exists(checkpoint_dir) else []
            
            resume_checkpoint = None
            starting_batch = 0
            
            if checkpoints:
                # Find the latest checkpoint
                latest_checkpoint = max(checkpoints, key=lambda x: int(x.split('_')[1].split('.')[0]))
                resume_checkpoint = os.path.join(checkpoint_dir, latest_checkpoint)
                starting_batch = int(latest_checkpoint.split('_')[1].split('.')[0]) + 1
                logger.info(f"Found checkpoint {latest_checkpoint}, resuming from batch {starting_batch}")
        else:
            resume_checkpoint = None
            starting_batch = 0
        
        # Initialize the processor
        processor = RulexBatchProcessor(
            model=model,
            X_train=X_train,
            feature_names=feature_names,
            output_dir=args.output_dir,
            batch_size=args.batch_size,
            n_jobs=args.n_jobs,
            checkpoint_frequency=args.checkpoint_freq,
            saved_explainer_path=args.explainer_path
        )
        
        # Process the dataset
        explanations = processor.process_dataset(
            X_all,
            starting_batch=starting_batch,
            resume_from_checkpoint=resume_checkpoint,
            save_explainer_frequency=10
        )
        
        # Save the results
        output_file = processor.save_explanations(explanations)
        summary_file = processor.generate_summary_report(explanations)
        
        logger.info("Batch processing complete!")
        logger.info(f"Explanations saved to: {output_file}")
        logger.info(f"Summary report: {summary_file}")
        
    else:
        # Demo mode - use simulated data
        logger.info("Running in demo mode with simulated data...")
        logger.info("Loading model and dataset...")
        
        # Check if required ML libraries are installed
        try:
            from catboost import CatBoostClassifier
        except ImportError:
            logger.warning("CatBoost not installed. Installing it now...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "catboost"])
        
        try:
            from autogluon.tabular import TabularPredictor
        except ImportError:
            logger.warning("AutoGluon not installed. Installing it now...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "autogluon"])
        
        # Create a dummy dataset and model for demonstration
    
    # Create a dummy dataset and model for demonstration
    np.random.seed(42)
    n_samples = 10_000_000  # 10M records
    n_features = 20
    
    # Create features in batches to avoid memory issues
    batch_size = 100_000
    n_batches = n_samples // batch_size
    
    # Create an empty array to simulate the dataset
    # In practice, you might use a generator or load from disk in chunks
    logger.info("Creating simulated large dataset...")
    X_all = np.empty((n_samples, n_features))
    y_all = np.empty(n_samples)
    
    for i in tqdm(range(n_batches)):
        start_idx = i * batch_size
        end_idx = (i + 1) * batch_size
        
        # Generate this batch
        X_batch = np.random.randn(batch_size, n_features)
        
        # Simple function to determine class
        y_batch = (X_batch[:, 0] + X_batch[:, 1] > 0).astype(int)
        
        # Store in the full arrays
        X_all[start_idx:end_idx] = X_batch
        y_all[start_idx:end_idx] = y_batch
    
    # Create feature names
    feature_names = [f"feature_{i}" for i in range(n_features)]
    
    # For demonstration, we'll train on a small subset
    logger.info("Training a sample model...")
    sample_size = 100_000  # Train on a smaller subset
    X_train = X_all[:sample_size]
    y_train = y_all[:sample_size]
    
    # Create and train an ensemble model (RandomForest + CatBoost + AutoGluon)
    logger.info("Training RandomForest model...")
    rf_model = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42)
    rf_model.fit(X_train, y_train)

    logger.info("Training CatBoost model...")
    from catboost import CatBoostClassifier
    catboost_model = CatBoostClassifier(
        iterations=100,
        depth=5,
        learning_rate=0.1,
        loss_function='Logloss',
        random_seed=42,
        verbose=False
    )
    catboost_model.fit(X_train, y_train)

    logger.info("Training AutoGluon model...")
    # Create a pandas DataFrame for AutoGluon
    import pandas as pd
    train_df = pd.DataFrame(X_train)
    train_df.columns = [f"feature_{i}" for i in range(X_train.shape[1])]
    train_df['target'] = y_train

    # Create a temporary directory for AutoGluon
    import tempfile
    ag_path = tempfile.mkdtemp()

    # Import AutoGluon
    try:
        from autogluon.tabular import TabularPredictor
    except ImportError:
        logger.warning("AutoGluon not installed. Installing it now...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "autogluon"])
        from autogluon.tabular import TabularPredictor

    # Train AutoGluon with minimal settings
    ag_model = TabularPredictor(
        label='target',
        path=ag_path,
        eval_metric='accuracy'
    )
    ag_model.fit(
        train_data=train_df,
        time_limit=300,  # 5 minutes time limit
        presets='medium_quality'
    )

    # Create the ensemble model that averages predictions
    class EnsembleModel:
        def __init__(self, rf_model, catboost_model, ag_model, ag_feature_names):
            self.rf_model = rf_model
            self.catboost_model = catboost_model
            self.ag_model = ag_model
            self.ag_feature_names = ag_feature_names
            
        def predict(self, X):
            """Make binary predictions using the ensemble"""
            probs = self.predict_proba(X)
            return np.argmax(probs, axis=1)
            
        def predict_proba(self, X):
            """
            Average probability predictions from all models
            """
            # Get RandomForest probabilities
            rf_probs = self.rf_model.predict_proba(X)
            
            # Get CatBoost probabilities
            catboost_probs = self.catboost_model.predict_proba(X)
            
            # Get AutoGluon probabilities
            # Convert to DataFrame with proper column names
            X_df = pd.DataFrame(X)
            X_df.columns = self.ag_feature_names
            ag_probs = self.ag_model.predict_proba(X_df).values
            
            # Average all probabilities
            avg_probs = (rf_probs + catboost_probs + ag_probs) / 3
            
            return avg_probs

    # Create the actual ensemble model
    model = EnsembleModel(
        catboost_model=catboost_model,
        ag_model=ag_model,
        ag_feature_names=[f"feature_{i}" for i in range(X_train.shape[1])]
    )
    
    # 2. Initialize the batch processor
    saved_explainer_path = os.path.join("rulex_explanations", "explainer", "rulex_explainer.pkl")
    
    processor = RulexBatchProcessor(
        model=model,
        X_train=X_train,
        feature_names=feature_names,
        batch_size=50000,  # Process 50k records per batch
        n_jobs=8,  # Use 8 cores (adjust for your system)
        checkpoint_frequency=5,  # Save checkpoint every 5 batches
        saved_explainer_path=saved_explainer_path if os.path.exists(saved_explainer_path) else None
    )
    
    # 3. Process the dataset
    logger.info("Starting batch processing...")
    
    # Check if we need to resume from a checkpoint
    checkpoint_dir = os.path.join("rulex_explanations", "checkpoints")
    checkpoints = [f for f in os.listdir(checkpoint_dir) if f.startswith("batch_") and f.endswith(".pkl")] if os.path.exists(checkpoint_dir) else []
    
    resume_checkpoint = None
    starting_batch = 0
    
    if checkpoints:
        # Find the latest checkpoint
        latest_checkpoint = max(checkpoints, key=lambda x: int(x.split('_')[1].split('.')[0]))
        resume_checkpoint = os.path.join(checkpoint_dir, latest_checkpoint)
        starting_batch = int(latest_checkpoint.split('_')[1].split('.')[0]) + 1
        logger.info(f"Found checkpoint {latest_checkpoint}, resuming from batch {starting_batch}")
    
    explanations = processor.process_dataset(
        X_all, 
        starting_batch=starting_batch,
        resume_from_checkpoint=resume_checkpoint,
        save_explainer_frequency=10  # Save explainer every 10 batches
    )
    
    # 4. Save explanations
    output_file = processor.save_explanations(explanations)
    
    # 5. Generate summary report
    summary_file = processor.generate_summary_report(explanations)
    
    logger.info("Batch processing complete!")
    logger.info(f"Explanations saved to: {output_file}")
    logger.info(f"Summary report: {summary_file}")
