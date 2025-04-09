#!/usr/bin/env python
# Batch Processing with RulexAI for Large-Scale Model Interpretability

import os
import pandas as pd
import numpy as np
import pickle
import time
from datetime import datetime
import logging
from tqdm import tqdm
# Import correct RuleKit and RulexAI packages
from rulekit import RuleKit
from rulekit.classification import RuleClassifier
from rulekit.params import Measures
from rulexai.explainer import Explainer
from joblib import Parallel, delayed, parallel_backend
import multiprocessing
import shutil
import sys
import tempfile

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

# Initialize directories for outputs
def init_directories(output_dir="rulex_explanations"):
    """Create necessary directories for output"""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f"{output_dir}/checkpoints", exist_ok=True)
    os.makedirs(f"{output_dir}/explainer", exist_ok=True)
    return output_dir

# Save RulexAI explainer to disk
def save_explainer(explainer, output_dir, filename="rulex_explainer.pkl"):
    """Save the RulexAI explainer object to disk"""
    filepath = os.path.join(output_dir, "explainer", filename)
    with open(filepath, 'wb') as f:
        pickle.dump(explainer, f)
    logger.info(f"RulexAI explainer saved to: {filepath}")
    return filepath

# Load RulexAI explainer from disk
def load_explainer(filepath):
    """Load a RulexAI explainer object from disk"""
    with open(filepath, 'rb') as f:
        explainer = pickle.load(f)
    logger.info(f"RulexAI explainer loaded from: {filepath}")
    return explainer

# Save checkpoint of batch results
def save_checkpoint(batch_results, batch_num, output_dir):
    """Save checkpoint of batch results"""
    checkpoint_path = f"{output_dir}/checkpoints/batch_{batch_num}.pkl"
    with open(checkpoint_path, 'wb') as f:
        pickle.dump(batch_results, f)
    logger.info(f"Checkpoint saved: {checkpoint_path}")
    return checkpoint_path

# Process a single record
def process_single_record(idx, X_record, explainer):
    """Process a single record and return its explanation"""
    try:
        # Generate explanation for this record
        # Using RulexAI's explain_instance method
        explanation = explainer.explain(X_record)
        return idx, explanation
    except Exception as e:
        logger.error(f"Error processing record {idx}: {str(e)}")
        return idx, None

# Process a batch of records in parallel
def process_batch(batch_indices, X_batch, explainer, batch_num, n_jobs, output_dir, checkpoint_frequency):
    """Process a batch of records in parallel"""
    logger.info(f"Processing batch {batch_num}: {len(batch_indices)} records")
    start_time = time.time()
    
    results = []
    with parallel_backend('loky', n_jobs=n_jobs):
        results = Parallel(verbose=1)(
            delayed(process_single_record)(idx, X_batch[i], explainer) 
            for i, idx in enumerate(batch_indices)
        )
        
    # Filter out failed explanations
    valid_results = [(idx, exp) for idx, exp in results if exp is not None]
    
    elapsed = time.time() - start_time
    logger.info(f"Batch {batch_num} processed in {elapsed:.2f}s " +
                f"({len(valid_results)}/{len(batch_indices)} successful)")
    
    # Save checkpoint if needed
    if batch_num % checkpoint_frequency == 0:
        save_checkpoint(valid_results, batch_num, output_dir)
        
    return valid_results

# Process the entire dataset
def process_dataset(model, X_train, X_to_explain, feature_names, 
                   batch_size=10000, n_jobs=-1, output_dir="rulex_explanations", 
                   checkpoint_frequency=5, starting_batch=0, resume_from_checkpoint=None,
                   save_explainer_frequency=20, saved_explainer_path=None):
    """
    Process the entire dataset in batches
    
    Args:
        model: The trained ensemble model to explain (with predict/predict_proba functions)
        X_train: Training data used for the model
        X_to_explain: The dataset to generate explanations for
        feature_names: List of feature names
        batch_size: Number of records to process in each batch
        n_jobs: Number of parallel jobs (-1 for all cores)
        output_dir: Directory to store explanations
        checkpoint_frequency: How often to save checkpoints (in batches)
        starting_batch: Batch number to start processing from
        resume_from_checkpoint: Path to checkpoint to resume from
        save_explainer_frequency: How often to save the explainer (in batches)
        saved_explainer_path: Path to a saved RulexAI explainer (if available)
    
    Returns:
        Dictionary of explanations (record index -> explanation)
    """
    # Initialize directories
    output_dir = init_directories(output_dir)
    
    # Set number of jobs for parallel processing
    n_jobs = n_jobs if n_jobs > 0 else multiprocessing.cpu_count()
    
    # Disable GPU to ensure CPU-only processing
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    
    # Define a wrapper class to make functional model compatible with RulexAI
    # This is needed only if the model is a dictionary with functions
    if isinstance(model, dict) and 'predict' in model and 'predict_proba' in model:
        class ModelWrapper:
            def __init__(self, model_dict):
                self.model_dict = model_dict
                
            def predict(self, X):
                return self.model_dict['predict'](X)
                
            def predict_proba(self, X):
                return self.model_dict['predict_proba'](X)
        
        model_wrapper = ModelWrapper(model)
    else:
        # If it's already a model object with methods, use it directly
        model_wrapper = model
    
    # Load or initialize RulexAI explainer
    if saved_explainer_path and os.path.exists(saved_explainer_path):
        logger.info(f"Loading saved RulexAI explainer from {saved_explainer_path}")
        explainer = load_explainer(saved_explainer_path)
    else:
        logger.info("Initializing new RulexAI explainer...")
        # Create a RuleKit classifier for use with RulexAI
        rule_classifier = RuleClassifier(
            min_rule_covered=5,
            induction_measure=Measures.Correlation,
            pruning_measure=Measures.Correlation,
            voting_measure=Measures.Correlation,
            max_growing=10000
        )
        
        # Initialize the Explainer with our ensemble model and the rule classifier
        explainer = Explainer(
            estimator=model_wrapper,
            rule_generator=rule_classifier,
            X_train=X_train,
            feature_names=feature_names
        )
        
        # Save the initial explainer
        save_explainer(explainer, output_dir)
    
    # Calculate total batches
    total_records = len(X_to_explain)
    total_batches = (total_records + batch_size - 1) // batch_size
    
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
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, total_records)
        
        batch_indices = list(range(start_idx, end_idx))
        X_batch = X_to_explain[start_idx:end_idx]
        
        # Process this batch
        batch_results = process_batch(
            batch_indices, X_batch, explainer, batch_num, 
            n_jobs, output_dir, checkpoint_frequency
        )
        
        # Add to overall results
        for idx, exp in batch_results:
            all_explanations[idx] = exp
            
        # Save progress report
        completion_percentage = (batch_num + 1) / total_batches * 100
        logger.info(f"Progress: {completion_percentage:.2f}% complete " +
                   f"({batch_num + 1}/{total_batches} batches)")
        
        # Periodically save the explainer object to capture any learning/updates
        if batch_num % save_explainer_frequency == 0:
            explainer_path = save_explainer(
                explainer, output_dir, f"rulex_explainer_batch_{batch_num}.pkl"
            )
            logger.info(f"Saved explainer snapshot at batch {batch_num}: {explainer_path}")
    
    logger.info(f"Batch processing complete. Successful explanations: {len(all_explanations)}")
    return all_explanations

# Save explanations to disk
def save_explanations(explanations, output_dir, filename="explanations.pkl"):
    """Save all explanations to disk"""
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'wb') as f:
        pickle.dump(explanations, f)
    logger.info(f"Explanations saved to: {filepath}")
    return filepath

# Generate a summary report from explanations
def generate_summary_report(explanations, output_dir):
    """Generate a summary report of the explanations"""
    # Count rule frequencies across all explanations
    rule_counts = {}
    total_explanations = len(explanations)
    
    for idx, explanation in explanations.items():
        # Extract rules from the explanation
        # Structure may vary based on RulexAI, adjusting as needed
        try:
            rules = explanation.get_rules()
            for rule in rules:
                rule_text = str(rule)
                if rule_text in rule_counts:
                    rule_counts[rule_text] += 1
                else:
                    rule_counts[rule_text] = 1
        except:
            # If rule extraction fails, continue with the next explanation
            continue
    
    # Sort rules by frequency
    sorted_rules = sorted(rule_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Save summary to file
    report_path = f"{output_dir}/summary_report.txt"
    with open(report_path, 'w') as f:
        f.write(f"RulexAI Explanation Summary\n")
        f.write(f"Generated on: {datetime.now()}\n")
        f.write(f"Total Records Processed: {total_explanations}\n\n")
        
        f.write(f"Top 20 Most Frequent Rules:\n")
        for i, (rule, count) in enumerate(sorted_rules[:20], 1):
            percentage = (count / total_explanations) * 100
            f.write(f"{i}. Rule: {rule}\n   Frequency: {count} ({percentage:.2f}%)\n\n")
        
        # Add more summary statistics as needed
    
    logger.info(f"Summary report generated: {report_path}")
    return report_path

# Create an ensemble model from CatBoost and AutoGluon using a functional approach
def create_ensemble_model(X_train, y_train, feature_names):
    """
    Create and train an ensemble model consisting of CatBoost and AutoGluon.
    Returns functions for prediction and probability estimation.
    
    Args:
        X_train: Training data features
        y_train: Training data labels
        feature_names: List of feature names
        
    Returns:
        A dictionary containing the models and prediction functions
    """
    import numpy as np
    import pandas as pd
    import tempfile
    import sys
    
    logger.info("Training ensemble model components...")
    
    # Train CatBoost
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
    
    # Create a pandas DataFrame for AutoGluon
    train_df = pd.DataFrame(X_train)
    train_df.columns = feature_names
    train_df['target'] = y_train
    
    # Train AutoGluon
    logger.info("Training AutoGluon model...")
    # Create a temporary directory for AutoGluon
    ag_path = tempfile.mkdtemp()
    
    # Import AutoGluon
    try:
        from autogluon.tabular import TabularPredictor
    except ImportError:
        logger.warning("AutoGluon not installed. Installing it now...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "autogluon"])
        from autogluon.tabular import TabularPredictor
    
    # Train AutoGluon with minimal settings for demonstration
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
    
    # Define ensemble prediction function for class labels
    def predict(X):
        """Make binary predictions using the ensemble"""
        probs = predict_proba(X)
        return np.argmax(probs, axis=1)
    
    # Define ensemble prediction function for probabilities    
    def predict_proba(X):
        """Average probability predictions from both models"""
        # Get CatBoost probabilities
        catboost_probs = catboost_model.predict_proba(X)
        
        # Get AutoGluon probabilities
        X_df = pd.DataFrame(X)
        X_df.columns = feature_names
        ag_probs = ag_model.predict_proba(X_df).values
        
        # Average the probabilities
        avg_probs = (catboost_probs + ag_probs) / 2
        
        return avg_probs
    
    # Create the ensemble model as a dictionary containing models and functions
    ensemble = {
        'catboost_model': catboost_model,
        'ag_model': ag_model,
        'feature_names': feature_names,
        'predict': predict,
        'predict_proba': predict_proba
    }
    
    logger.info("Ensemble model created and trained successfully")
    return ensemble

# Find the latest checkpoint
def find_latest_checkpoint(checkpoint_dir):
    """Find the latest checkpoint file and determine starting batch"""
    checkpoints = [f for f in os.listdir(checkpoint_dir) if f.startswith("batch_") and f.endswith(".pkl")] if os.path.exists(checkpoint_dir) else []
    
    if not checkpoints:
        return None, 0
        
    # Find the latest checkpoint
    latest_checkpoint = max(checkpoints, key=lambda x: int(x.split('_')[1].split('.')[0]))
    resume_checkpoint = os.path.join(checkpoint_dir, latest_checkpoint)
    starting_batch = int(latest_checkpoint.split('_')[1].split('.')[0]) + 1
    
    return resume_checkpoint, starting_batch

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
    # Check if running in demo mode or CLI mode
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
        
        # Check if all required ML libraries are installed
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
        
        # Determine if we should resume from a checkpoint
        resume_checkpoint = None
        starting_batch = 0
        
        if args.resume:
            checkpoint_dir = os.path.join(args.output_dir, "checkpoints")
            resume_checkpoint, starting_batch = find_latest_checkpoint(checkpoint_dir)
            if resume_checkpoint:
                logger.info(f"Found checkpoint, resuming from batch {starting_batch}")
            else:
                logger.info("No checkpoints found, starting from the beginning")
                
        # Process the dataset
        explanations = process_dataset(
            model=model,
            X_train=X_train,
            X_to_explain=X_all,
            feature_names=feature_names,
            batch_size=args.batch_size,
            n_jobs=args.n_jobs,
            output_dir=args.output_dir,
            checkpoint_frequency=args.checkpoint_freq,
            starting_batch=starting_batch,
            resume_from_checkpoint=resume_checkpoint,
            save_explainer_frequency=10,
            saved_explainer_path=args.explainer_path
        )
        
        # Save the results
        output_file = save_explanations(explanations, args.output_dir)
        summary_file = generate_summary_report(explanations, args.output_dir)
        
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
        
        # Create and train the ensemble model (CatBoost + AutoGluon)
        model = create_ensemble_model(X_train, y_train, feature_names)
        
        # Save the ensemble model
        output_dir = init_directories()
        ensemble_path = os.path.join(output_dir, "ensemble_model.pkl")
        with open(ensemble_path, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"Ensemble model saved to: {ensemble_path}")
        
        # Check for existing checkpoints to resume from
        checkpoint_dir = os.path.join(output_dir, "checkpoints")
        resume_checkpoint, starting_batch = find_latest_checkpoint(checkpoint_dir)
        
        if resume_checkpoint:
            logger.info(f"Found checkpoint {os.path.basename(resume_checkpoint)}, resuming from batch {starting_batch}")
        else:
            logger.info("No checkpoints found, starting from the beginning")
        
        # Process the dataset
        explanations = process_dataset(
            model=model,
            X_train=X_train,
            X_to_explain=X_all,
            feature_names=feature_names,
            batch_size=50000,  # Process 50k records per batch
            n_jobs=8,  # Use 8 cores (adjust for your system)
            output_dir=output_dir,
            checkpoint_frequency=5,  # Save checkpoint every 5 batches
            starting_batch=starting_batch,
            resume_from_checkpoint=resume_checkpoint,
            save_explainer_frequency=10  # Save explainer every 10 batches
        )
        
        # Save the results
        output_file = save_explanations(explanations, output_dir)
        summary_file = generate_summary_report(explanations, output_dir)
        
        logger.info("Batch processing complete!")
        logger.info(f"Explanations saved to: {output_file}")
        logger.info(f"Summary report: {summary_file}")
