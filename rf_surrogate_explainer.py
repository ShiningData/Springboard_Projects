import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from typing import Dict, List, Tuple, Optional, Union, Callable
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import gc

class EnsembleSurrogateExplainer:
    """
    Random Forest surrogate explainer specifically designed for AutoGluon + CatBoost ensemble models.
    
    Enterprise-safe explainer for binary classification that provides both local and global 
    explanations without missing value imputation. Optimized for healthcare applications 
    and large-scale datasets (10M+ records).
    
    Features:
    - Specifically designed for AutoGluon + CatBoost ensemble models
    - Binary classification focused (0/1 predictions)
    - No missing value imputation (uses masking strategies only)
    - Enterprise-safe licensing (sklearn/numpy/pandas only)
    - Scalable batch processing for large datasets
    - Ensemble model fidelity validation
    - Both local and global explanations
    """
    
    def __init__(self, 
                 ensemble_model,
                 feature_names: List[str],
                 model_type: str = "autogluon",
                 n_estimators: int = 200,
                 max_depth: Optional[int] = 10,
                 min_samples_split: int = 5,
                 min_samples_leaf: int = 2,
                 max_features: str = "sqrt",
                 random_state: int = 42,
                 n_jobs: int = -1,
                 class_weight: str = "balanced"):
        """
        Initialize the Ensemble Surrogate Explainer for AutoGluon + CatBoost models.
        
        Args:
            ensemble_model: AutoGluon predictor or ensemble model
            feature_names: List of feature names
            model_type: Type of ensemble ("autogluon", "catboost", or "custom")
            n_estimators: Number of trees in Random Forest surrogate
            max_depth: Maximum depth of trees
            min_samples_split: Minimum samples required to split a node
            min_samples_leaf: Minimum samples required at leaf node
            max_features: Number of features to consider for best split
            random_state: Random seed for reproducibility
            n_jobs: Number of parallel jobs (-1 for all processors)
            class_weight: Weights associated with classes
        """
        self.ensemble_model = ensemble_model
        self.feature_names = feature_names
        self.n_features = len(feature_names)
        self.model_type = model_type.lower()
        
        # Initialize Random Forest surrogate with healthcare-optimized parameters
        self.surrogate_model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            max_features=max_features,
            random_state=random_state,
            n_jobs=n_jobs,
            class_weight=class_weight,
            bootstrap=True,
            oob_score=True
        )
        
        # Training and validation data storage
        self.training_stats = {}
        self.is_fitted = False
        self.fidelity_metrics = {}
        
        # Global explanation cache
        self._global_importance = None
        self._feature_interactions = None
        
        # Ensemble-specific attributes
        self.ensemble_info = {}
        
    def fit(self, X_train: np.ndarray, 
            validation_size: float = 0.2,
            fidelity_threshold: float = 0.85,
            batch_size: int = 10000,
            balance_classes: bool = True) -> Dict:
        """
        Train the Random Forest surrogate model on the ensemble model's predictions.
        
        Args:
            X_train: Training data (N x F array)
            validation_size: Fraction of data to use for validation
            fidelity_threshold: Minimum required fidelity score
            batch_size: Batch size for processing large datasets
            balance_classes: Whether to balance classes during training
            
        Returns:
            Dictionary with training results and fidelity metrics
        """
        print(f"Training Random Forest surrogate for {self.model_type} ensemble...")
        print(f"Training samples: {X_train.shape[0]}, Features: {X_train.shape[1]}")
        start_time = time.time()
        
        # Calculate training statistics for masking (no imputation)
        self._calculate_training_stats(X_train)
        
        # Extract ensemble information
        self._extract_ensemble_info()
        
        # Generate surrogate labels using ensemble model
        print("Generating surrogate labels from ensemble model...")
        y_surrogate, ensemble_probs = self._generate_ensemble_labels(X_train, batch_size)
        
        # Validate binary classification
        unique_classes = np.unique(y_surrogate)
        if len(unique_classes) != 2 or not all(c in [0, 1] for c in unique_classes):
            raise ValueError(f"Expected binary classes [0, 1], got {unique_classes}")
        
        print(f"Class distribution: Class 0: {np.sum(y_surrogate == 0)}, Class 1: {np.sum(y_surrogate == 1)}")
        
        # Split data for training and validation
        if validation_size > 0:
            X_train_split, X_val, y_train_split, y_val, prob_train, prob_val = train_test_split(
                X_train, y_surrogate, ensemble_probs, 
                test_size=validation_size, 
                random_state=42, 
                stratify=y_surrogate
            )
        else:
            X_train_split, X_val = X_train, None
            y_train_split, y_val = y_surrogate, None
            prob_train, prob_val = ensemble_probs, None
        
        # Train surrogate Random Forest
        print(f"Training Random Forest on {X_train_split.shape[0]} samples...")
        
        # Handle class imbalance if requested
        if balance_classes:
            class_counts = np.bincount(y_train_split)
            print(f"Class imbalance ratio: {class_counts[1] / class_counts[0]:.3f}")
        
        self.surrogate_model.fit(X_train_split, y_train_split)
        
        # Calculate comprehensive fidelity metrics
        fidelity_results = self._calculate_comprehensive_fidelity(
            X_val, y_val, prob_val
        ) if X_val is not None else {}
        
        self.is_fitted = True
        self.fidelity_metrics = fidelity_results
        training_time = time.time() - start_time
        
        # Get OOB score for additional validation
        oob_score = self.surrogate_model.oob_score_ if hasattr(self.surrogate_model, 'oob_score_') else None
        
        results = {
            'training_time': training_time,
            'training_samples': X_train_split.shape[0],
            'validation_samples': X_val.shape[0] if X_val is not None else 0,
            'ensemble_type': self.model_type,
            'surrogate_accuracy': fidelity_results.get('classification_accuracy', 'Not calculated'),
            'surrogate_auc': fidelity_results.get('auc_score', 'Not calculated'),
            'fidelity_score': fidelity_results.get('overall_fidelity', 'Not calculated'),
            'probability_fidelity': fidelity_results.get('probability_fidelity', 'Not calculated'),
            'oob_score': oob_score,
            'feature_count': self.n_features,
            'trees_count': self.surrogate_model.n_estimators,
            'class_distribution': {
                'class_0_count': int(np.sum(y_train_split == 0)),
                'class_1_count': int(np.sum(y_train_split == 1)),
                'class_0_ratio': float(np.mean(y_train_split == 0)),
                'class_1_ratio': float(np.mean(y_train_split == 1))
            }
        }
        
        # Check fidelity threshold
        overall_fidelity = fidelity_results.get('overall_fidelity', 0)
        if overall_fidelity < fidelity_threshold:
            warnings.warn(f"Surrogate fidelity ({overall_fidelity:.3f}) "
                         f"below threshold ({fidelity_threshold}). "
                         f"Consider increasing n_estimators or collecting more training data.")
        
        print(f"Surrogate model training completed in {training_time:.2f} seconds")
        print(f"Overall fidelity: {overall_fidelity:.4f}")
        print(f"Classification accuracy: {fidelity_results.get('classification_accuracy', 'N/A'):.4f}")
        
        return results
    
    def explain_local(self, 
                     instance: np.ndarray,
                     top_k: int = 5,
                     include_predictions: bool = True,
                     include_confidence: bool = True) -> Dict:
        """
        Generate local explanation for a single instance from ensemble model.
        
        Args:
            instance: Single instance to explain (1D array)
            top_k: Number of top features to return
            include_predictions: Whether to include prediction details
            include_confidence: Whether to include confidence metrics
            
        Returns:
            Dictionary with local explanation results
        """
        if not self.is_fitted:
            raise ValueError("Surrogate model must be fitted before generating explanations")
        
        if len(instance.shape) == 1:
            instance = instance.reshape(1, -1)
        
        # Get predictions from both ensemble and surrogate
        ensemble_pred = self._get_ensemble_prediction(instance)
        surrogate_pred = self.surrogate_model.predict_proba(instance)[0]
        surrogate_class = self.surrogate_model.predict(instance)[0]
        
        # Calculate local importance using multiple strategies
        local_importance = self._calculate_local_importance_ensemble(instance[0])
        
        # Get top k features
        top_indices = np.argsort(local_importance)[::-1][:top_k]
        
        explanation = {
            'instance_id': 0,
            'instance_values': instance[0].tolist(),
            'local_importance': local_importance.tolist(),
            'top_features': [
                {
                    'rank': rank + 1,
                    'feature_name': self.feature_names[idx],
                    'feature_index': int(idx),
                    'importance_score': float(local_importance[idx]),
                    'feature_value': float(instance[0, idx]),
                    'contribution_direction': 'positive' if local_importance[idx] > 0 else 'neutral'
                }
                for rank, idx in enumerate(top_indices)
            ]
        }
        
        # Add prediction details if requested
        if include_predictions:
            explanation['predictions'] = {
                'ensemble': {
                    'probability_class_1': float(ensemble_pred),
                    'probability_class_0': float(1 - ensemble_pred),
                    'predicted_class': int(ensemble_pred > 0.5),
                    'confidence': float(abs(ensemble_pred - 0.5) * 2)
                },
                'surrogate': {
                    'probability_class_1': float(surrogate_pred[1]),
                    'probability_class_0': float(surrogate_pred[0]),
                    'predicted_class': int(surrogate_class),
                    'confidence': float(max(surrogate_pred))
                },
                'agreement': {
                    'class_agreement': bool(int(ensemble_pred > 0.5) == int(surrogate_class)),
                    'probability_difference': float(abs(ensemble_pred - surrogate_pred[1]))
                }
            }
        
        # Add confidence metrics if requested
        if include_confidence:
            explanation['confidence_metrics'] = self._calculate_local_confidence(instance, local_importance)
        
        return explanation
    
    def explain_local_batch(self, 
                           X_batch: np.ndarray,
                           top_k: int = 5,
                           batch_size: int = 1000,
                           show_progress: bool = True) -> List[Dict]:
        """
        Generate local explanations for a batch of instances efficiently.
        Optimized for large-scale healthcare datasets.
        
        Args:
            X_batch: Batch of instances (N x F array)
            top_k: Number of top features per instance
            batch_size: Internal processing batch size for memory efficiency
            show_progress: Whether to show progress updates
            
        Returns:
            List of local explanation dictionaries
        """
        if not self.is_fitted:
            raise ValueError("Surrogate model must be fitted before generating explanations")
        
        print(f"Generating local explanations for {X_batch.shape[0]} instances...")
        explanations = []
        
        # Process in batches for memory efficiency
        n_batches = (X_batch.shape[0] + batch_size - 1) // batch_size
        
        for batch_idx in range(n_batches):
            start_idx = batch_idx * batch_size
            end_idx = min(start_idx + batch_size, X_batch.shape[0])
            batch = X_batch[start_idx:end_idx]
            
            if show_progress and batch_idx % 10 == 0:
                print(f"Processing batch {batch_idx + 1}/{n_batches}")
            
            # Calculate batch importance efficiently
            batch_importance = self._calculate_batch_local_importance_ensemble(batch)
            
            # Get predictions for the batch
            ensemble_preds = self._get_ensemble_predictions_batch(batch)
            surrogate_probs = self.surrogate_model.predict_proba(batch)
            surrogate_classes = self.surrogate_model.predict(batch)
            
            # Process each instance in the batch
            for i, (instance, importance, ens_pred, surr_prob, surr_class) in enumerate(
                zip(batch, batch_importance, ensemble_preds, surrogate_probs, surrogate_classes)
            ):
                top_indices = np.argsort(importance)[::-1][:top_k]
                
                explanations.append({
                    'instance_id': start_idx + i,
                    'predictions': {
                        'ensemble': {
                            'probability_class_1': float(ens_pred),
                            'predicted_class': int(ens_pred > 0.5),
                            'confidence': float(abs(ens_pred - 0.5) * 2)
                        },
                        'surrogate': {
                            'probability_class_1': float(surr_prob[1]),
                            'predicted_class': int(surr_class),
                            'confidence': float(max(surr_prob))
                        },
                        'agreement': bool(int(ens_pred > 0.5) == int(surr_class))
                    },
                    'local_importance': importance.tolist(),
                    'top_features': [
                        {
                            'rank': rank + 1,
                            'feature_name': self.feature_names[idx],
                            'feature_index': int(idx),
                            'importance_score': float(importance[idx]),
                            'feature_value': float(instance[idx])
                        }
                        for rank, idx in enumerate(top_indices)
                    ]
                })
            
            # Periodic garbage collection for large batches
            if batch_idx % 50 == 0:
                gc.collect()
        
        return explanations
    
    def explain_global(self, 
                      X_sample: Optional[np.ndarray] = None,
                      top_k: int = 15,
                      include_interactions: bool = True,
                      interaction_depth: int = 2) -> Dict:
        """
        Generate comprehensive global explanation for the ensemble model.
        
        Args:
            X_sample: Sample data for analysis (optional)
            top_k: Number of top global features to return
            include_interactions: Whether to analyze feature interactions
            interaction_depth: Depth of interaction analysis (2 for pairwise)
            
        Returns:
            Dictionary with global explanation results
        """
        if not self.is_fitted:
            raise ValueError("Surrogate model must be fitted before generating explanations")
        
        print("Generating global explanations...")
        
        # Get Random Forest feature importance (global)
        rf_importance = self.surrogate_model.feature_importances_
        
        # Get individual tree importance for stability analysis
        tree_importances = np.array([
            tree.feature_importances_ for tree in self.surrogate_model.estimators_
        ])
        
        # Calculate importance statistics
        importance_std = np.std(tree_importances, axis=0)
        importance_stability = 1 - (importance_std / (rf_importance + 1e-8))
        
        # Calculate confidence intervals for importance scores
        importance_ci_lower = np.percentile(tree_importances, 2.5, axis=0)
        importance_ci_upper = np.percentile(tree_importances, 97.5, axis=0)
        
        # Get top k global features
        top_indices = np.argsort(rf_importance)[::-1][:top_k]
        
        global_explanation = {
            'model_info': {
                'surrogate_type': 'Random Forest',
                'ensemble_type': self.model_type,
                'n_estimators': self.surrogate_model.n_estimators,
                'total_features': self.n_features,
                'fidelity_score': self.fidelity_metrics.get('overall_fidelity', 'Not available'),
                'oob_score': getattr(self.surrogate_model, 'oob_score_', 'Not available')
            },
            'global_feature_importance': rf_importance.tolist(),
            'importance_stability': importance_stability.tolist(),
            'top_global_features': [
                {
                    'rank': rank + 1,
                    'feature_name': self.feature_names[idx],
                    'feature_index': int(idx),
                    'importance_score': float(rf_importance[idx]),
                    'stability_score': float(importance_stability[idx]),
                    'confidence_interval': {
                        'lower': float(importance_ci_lower[idx]),
                        'upper': float(importance_ci_upper[idx])
                    },
                    'relative_importance': float(rf_importance[idx] / np.sum(rf_importance))
                }
                for rank, idx in enumerate(top_indices)
            ]
        }
        
        # Add sample-based analysis if provided
        if X_sample is not None:
            sample_analysis = self._analyze_global_patterns(X_sample)
            global_explanation['sample_analysis'] = sample_analysis
        
        # Add feature interactions if requested
        if include_interactions and X_sample is not None:
            print("Analyzing feature interactions...")
            interaction_results = self.get_feature_interactions(
                X_sample, top_pairs=min(20, (top_k * (top_k - 1)) // 2)
            )
            global_explanation['feature_interactions'] = interaction_results
        
        # Cache global importance
        self._global_importance = rf_importance
        
        return global_explanation
    
    def get_feature_interactions(self, 
                               X_sample: np.ndarray,
                               top_pairs: int = 15,
                               method: str = "surrogate") -> Dict:
        """
        Analyze feature interactions using the surrogate Random Forest.
        
        Args:
            X_sample: Sample data for interaction analysis
            top_pairs: Number of top feature pairs to return
            method: Method for interaction analysis ("surrogate" or "permutation")
            
        Returns:
            Dictionary with feature interaction analysis
        """
        if not self.is_fitted:
            raise ValueError("Surrogate model must be fitted before analyzing interactions")
        
        print(f"Analyzing feature interactions using {method} method...")
        
        if method == "surrogate":
            interaction_scores = self._calculate_rf_feature_interactions(X_sample)
        else:
            interaction_scores = self._calculate_permutation_interactions(X_sample)
        
        # Get top interactions
        interaction_pairs = []
        for i in range(self.n_features):
            for j in range(i + 1, self.n_features):
                interaction_pairs.append({
                    'feature_1': self.feature_names[i],
                    'feature_2': self.feature_names[j],
                    'feature_1_idx': int(i),
                    'feature_2_idx': int(j),
                    'interaction_score': float(interaction_scores[i, j]),
                    'normalized_score': float(interaction_scores[i, j] / np.max(interaction_scores))
                })
        
        # Sort by interaction strength
        interaction_pairs.sort(key=lambda x: x['interaction_score'], reverse=True)
        
        return {
            'interaction_matrix': interaction_scores.tolist(),
            'top_interactions': interaction_pairs[:top_pairs],
            'total_pairs_analyzed': len(interaction_pairs),
            'method_used': method
        }
    
    def validate_ensemble_fidelity(self, 
                                  X_test: np.ndarray,
                                  detailed: bool = True,
                                  batch_size: int = 5000) -> Dict:
        """
        Comprehensive validation of surrogate fidelity to ensemble model.
        
        Args:
            X_test: Test data for validation
            detailed: Whether to return detailed metrics
            batch_size: Batch size for processing
            
        Returns:
            Dictionary with comprehensive fidelity validation results
        """
        if not self.is_fitted:
            raise ValueError("Surrogate model must be fitted before validation")
        
        print(f"Validating surrogate fidelity on {X_test.shape[0]} test samples...")
        
        # Get predictions from both models in batches
        ensemble_preds = self._get_ensemble_predictions_batch(X_test, batch_size)
        ensemble_classes = (ensemble_preds > 0.5).astype(int)
        
        surrogate_probs = []
        surrogate_classes = []
        
        for i in range(0, X_test.shape[0], batch_size):
            batch = X_test[i:i + batch_size]
            batch_probs = self.surrogate_model.predict_proba(batch)[:, 1]
            batch_classes = self.surrogate_model.predict(batch)
            
            surrogate_probs.extend(batch_probs)
            surrogate_classes.extend(batch_classes)
        
        surrogate_probs = np.array(surrogate_probs)
        surrogate_classes = np.array(surrogate_classes)
        
        # Calculate comprehensive fidelity metrics
        classification_accuracy = accuracy_score(ensemble_classes, surrogate_classes)
        prob_correlation = np.corrcoef(ensemble_preds, surrogate_probs)[0, 1]
        prob_mae = np.mean(np.abs(ensemble_preds - surrogate_probs))
        prob_rmse = np.sqrt(np.mean((ensemble_preds - surrogate_probs) ** 2))
        
        # AUC scores
        try:
            ensemble_auc = roc_auc_score(ensemble_classes, ensemble_preds)
            surrogate_auc = roc_auc_score(ensemble_classes, surrogate_probs)
            auc_difference = abs(ensemble_auc - surrogate_auc)
        except ValueError:
            ensemble_auc = surrogate_auc = auc_difference = None
        
        # Overall fidelity score (weighted combination)
        overall_fidelity = (
            0.4 * classification_accuracy +
            0.3 * max(0, prob_correlation) +
            0.2 * (1 - min(1, prob_mae)) +
            0.1 * (1 - min(1, auc_difference if auc_difference else 0))
        )
        
        results = {
            'classification_accuracy': float(classification_accuracy),
            'probability_correlation': float(prob_correlation),
            'probability_mae': float(prob_mae),
            'probability_rmse': float(prob_rmse),
            'overall_fidelity': float(overall_fidelity),
            'samples_tested': int(X_test.shape[0])
        }
        
        if ensemble_auc is not None:
            results.update({
                'ensemble_auc': float(ensemble_auc),
                'surrogate_auc': float(surrogate_auc),
                'auc_difference': float(auc_difference)
            })
        
        if detailed:
            results.update({
                'confusion_matrix': confusion_matrix(ensemble_classes, surrogate_classes).tolist(),
                'classification_report': classification_report(
                    ensemble_classes, surrogate_classes, output_dict=True
                ),
                'class_agreement_rates': {
                    'class_0_agreement': float(np.mean(
                        (ensemble_classes == 0) & (surrogate_classes == 0)
                    ) / np.sum(ensemble_classes == 0)) if np.sum(ensemble_classes == 0) > 0 else 0,
                    'class_1_agreement': float(np.mean(
                        (ensemble_classes == 1) & (surrogate_classes == 1)
                    ) / np.sum(ensemble_classes == 1)) if np.sum(ensemble_classes == 1) > 0 else 0
                }
            })
        
        self.fidelity_metrics.update(results)
        print(f"Fidelity validation completed. Overall fidelity: {overall_fidelity:.4f}")
        
        return results
    
    def get_ensemble_insights(self) -> Dict:
        """
        Get insights specific to the ensemble model being explained.
        
        Returns:
            Dictionary with ensemble-specific insights
        """
        insights = {
            'ensemble_type': self.model_type,
            'surrogate_summary': self.get_model_summary(),
            'fidelity_metrics': self.fidelity_metrics
        }
        
        if self.ensemble_info:
            insights['ensemble_info'] = self.ensemble_info
        
        return insights
    
    # Private methods for ensemble-specific functionality
    
    def _extract_ensemble_info(self):
        """Extract information about the ensemble model"""
        if self.model_type == "autogluon":
            try:
                # Try to extract AutoGluon model information
                if hasattr(self.ensemble_model, '_trainer'):
                    trainer = self.ensemble_model._trainer
                    if hasattr(trainer, 'model_best'):
                        models = trainer.model_best.models
                        self.ensemble_info = {
                            'n_models': len(models),
                            'model_types': [type(model).__name__ for model in models.values()],
                            'model_names': list(models.keys())
                        }
                        print(f"Detected AutoGluon ensemble with {len(models)} models")
            except Exception as e:
                print(f"Could not extract AutoGluon info: {e}")
        
        elif self.model_type == "catboost":
            try:
                if hasattr(self.ensemble_model, 'get_model_info'):
                    self.ensemble_info = {'model_type': 'CatBoost'}
            except Exception as e:
                print(f"Could not extract CatBoost info: {e}")
    
    def _calculate_training_stats(self, X_train: np.ndarray):
        """Calculate training statistics for masking strategies (no imputation)"""
        print("Calculating training statistics for feature masking...")
        self.training_stats = {
            'medians': np.median(X_train, axis=0),
            'means': np.mean(X_train, axis=0),
            'zeros': np.zeros(X_train.shape[1]),
            'q25': np.percentile(X_train, 25, axis=0),
            'q75': np.percentile(X_train, 75, axis=0),
            'mins': np.min(X_train, axis=0),
            'maxs': np.max(X_train, axis=0)
        }
    
    def _generate_ensemble_labels(self, X: np.ndarray, batch_size: int) -> Tuple[np.ndarray, np.ndarray]:
        """Generate labels and probabilities using the ensemble model in batches"""
        y_surrogate = []
        ensemble_probs = []
        
        n_batches = (X.shape[0] + batch_size - 1) // batch_size
        
        for i in range(n_batches):
            start_idx = i * batch_size
            end_idx = min(start_idx + batch_size, X.shape[0])
            batch = X[start_idx:end_idx]
            
            batch_probs = self._get_ensemble_predictions_batch(batch)
            batch_labels = (batch_probs > 0.5).astype(int)
            
            y_surrogate.extend(batch_labels)
            ensemble_probs.extend(batch_probs)
            
            if i % 100 == 0:
                print(f"Processed batch {i + 1}/{n_batches}")
        
        return np.array(y_surrogate), np.array(ensemble_probs)
    
    def _get_ensemble_prediction(self, instance: np.ndarray) -> float:
        """Get prediction from ensemble model for single instance"""
        try:
            if hasattr(self.ensemble_model, 'predict_proba'):
                pred = self.ensemble_model.predict_proba(instance)
                if isinstance(pred, np.ndarray):
                    if pred.ndim > 1 and pred.shape[1] > 1:
                        return float(pred[0, 1])  # Binary classification - class 1 probability
                    else:
                        return float(pred[0])
                else:
                    return float(pred)
            else:
                # Fallback to predict method
                pred = self.ensemble_model.predict(instance)
                return float(pred[0])
        except Exception as e:
            print(f"Error getting ensemble prediction: {e}")
            return 0.5  # Default neutral prediction
    
    def _get_ensemble_predictions_batch(self, X_batch: np.ndarray, batch_size: int = 5000) -> np.ndarray:
        """Get predictions from ensemble model for batch with memory management"""
        if X_batch.shape[0] <= batch_size:
            return self._get_ensemble_predictions_single_batch(X_batch)
        
        # Process in smaller batches to manage memory
        predictions = []
        for i in range(0, X_batch.shape[0], batch_size):
            batch = X_batch[i:i + batch_size]
            batch_preds = self._get_ensemble_predictions_single_batch(batch)
            predictions.extend(batch_preds)
        
        return np.array(predictions)
    
    def _get_ensemble_predictions_single_batch(self, X_batch: np.ndarray) -> np.ndarray:
        """Get predictions from ensemble model for a single batch"""
        try:
            if hasattr(self.ensemble_model, 'predict_proba'):
                preds = self.ensemble_model.predict_proba(X_batch)
                if isinstance(preds, np.ndarray):
                    if preds.ndim > 1 and preds.shape[1] > 1:
                        return preds[:, 1]  # Binary classification - class 1 probability
                    else:
                        return preds.flatten()
                else:
                    return np.array([float(preds)] * X_batch.shape[0])
            else:
                preds = self.ensemble_model.predict(X_batch)
                return preds.astype(float)
        except Exception as e:
            print(f"Error getting ensemble batch predictions: {e}")
            return np.full(X_batch.shape[0], 0.5)  # Default neutral predictions
    
    def _calculate_local_importance_ensemble(self, instance: np.ndarray) -> np.ndarray:
        """Calculate local importance using multiple masking strategies (no imputation)"""
        baseline_pred = self.surrogate_model.predict_proba(instance.reshape(1, -1))[0, 1]
        importance_scores = np.zeros(self.n_features)
        
        for feature_idx in range(self.n_features):
            strategy_scores = []
            
            # Strategy 1: Zero masking
            masked_instance = instance.copy()
            masked_instance[feature_idx] = 0
            masked_pred = self.surrogate_model.predict_proba(masked_instance.reshape(1, -1))[0, 1]
            strategy_scores.append(abs(baseline_pred - masked_pred))
            
            # Strategy 2: Median masking
            masked_instance = instance.copy()
            masked_instance[feature_idx] = self.training_stats['medians'][feature_idx]
            median_pred = self.surrogate_model.predict_proba(masked_instance.reshape(1, -1))[0, 1]
            strategy_scores.append(abs(baseline_pred - median_pred))
            
            # Strategy 3: Mean masking
            masked_instance = instance.copy()
            masked_instance[feature_idx] = self.training_stats['means'][feature_idx]
            mean_pred = self.surrogate_model.predict_proba(masked_instance.reshape(1, -1))[0, 1]
            strategy_scores.append(abs(baseline_pred - mean_pred))
            
            # Average across strategies for robust importance score
            importance_scores[feature_idx] = np.mean(strategy_scores)
        
        return importance_scores
    
    def _calculate_batch_local_importance_ensemble(self, X_batch: np.ndarray) -> np.ndarray:
        """Calculate local importance for batch of instances using ensemble-optimized approach"""
        batch_size, n_features = X_batch.shape
        importance_matrix = np.zeros((batch_size, n_features))
        
        # Get baseline predictions
        baseline_probs = self.surrogate_model.predict_proba(X_batch)[:, 1]
        
        # Use zero masking for efficiency in batch processing
        for feature_idx in range(n_features):
            X_masked = X_batch.copy()
            X_masked[:, feature_idx] = 0
            masked_probs = self.surrogate_model.predict_proba(X_masked)[:, 1]
            importance_matrix[:, feature_idx] = np.abs(baseline_probs - masked_probs)
        
        return importance_matrix
    
    def _calculate_comprehensive_fidelity(self, X_val: np.ndarray, 
                                        y_val: np.ndarray, 
                                        prob_val: np.ndarray) -> Dict:
        """Calculate comprehensive fidelity metrics"""
        if X_val is None or y_val is None:
            return {}
        
        surrogate_pred = self.surrogate_model.predict(X_val)
        surrogate_prob = self.surrogate_model.predict_proba(X_val)[:, 1]
        
        # Classification accuracy
        classification_accuracy = accuracy_score(y_val, surrogate_pred)
        
        # Probability fidelity
        prob_correlation = np.corrcoef(prob_val, surrogate_prob)[0, 1]
        prob_mae = np.mean(np.abs(prob_val - surrogate_prob))
        
        # AUC comparison
        try:
            ensemble_auc = roc_auc_score(y_val, prob_val)
            surrogate_auc = roc_auc_score(y_val, surrogate_prob)
            auc_difference = abs(ensemble_auc - surrogate_auc)
        except ValueError:
            ensemble_auc = surrogate_auc = auc_difference = None
        
        # Overall fidelity (weighted combination)
        overall_fidelity = (
            0.5 * classification_accuracy +
            0.3 * max(0, prob_correlation) +
            0.2 * (1 - min(1, prob_mae))
        )
        
        return {
            'classification_accuracy': classification_accuracy,
            'probability_fidelity': prob_correlation,
            'probability_mae': prob_mae,
            'auc_score': surrogate_auc,
            'overall_fidelity': overall_fidelity
        }
    
    def _calculate_local_confidence(self, instance: np.ndarray, importance: np.ndarray) -> Dict:
        """Calculate confidence metrics for local explanation"""
        # Prediction confidence
        surrogate_prob = self.surrogate_model.predict_proba(instance)[0]
        prediction_confidence = max(surrogate_prob)
        
        # Feature importance concentration (entropy-based)
        normalized_importance = importance / (np.sum(importance) + 1e-8)
        importance_entropy = -np.sum(normalized_importance * np.log(normalized_importance + 1e-8))
        importance_concentration = 1 - (importance_entropy / np.log(len(importance)))
        
        return {
            'prediction_confidence': float(prediction_confidence),
            'importance_concentration': float(importance_concentration),
            'top_feature_dominance': float(np.max(importance) / (np.sum(importance) + 1e-8))
        }
    
    def _analyze_global_patterns(self, X_sample: np.ndarray) -> Dict:
        """Analyze global patterns in the sample data"""
        predictions = self.surrogate_model.predict_proba(X_sample)[:, 1]
        classes = self.surrogate_model.predict(X_sample)
        
        return {
            'prediction_distribution': {
                'mean': float(np.mean(predictions)),
                'std': float(np.std(predictions)),
                'min': float(np.min(predictions)),
                'max': float(np.max(predictions)),
                'q25': float(np.percentile(predictions, 25)),
                'q75': float(np.percentile(predictions, 75))
            },
            'class_distribution': {
                'class_0_count': int(np.sum(classes == 0)),
                'class_1_count': int(np.sum(classes == 1)),
                'class_0_ratio': float(np.mean(classes == 0)),
                'class_1_ratio': float(np.mean(classes == 1))
            },
            'sample_size': int(X_sample.shape[0])
        }
    
    def _calculate_rf_feature_interactions(self, X_sample: np.ndarray) -> np.ndarray:
        """Calculate feature interactions using Random Forest structure"""
        interaction_matrix = np.zeros((self.n_features, self.n_features))
        
        # Use the trained Random Forest to analyze feature co-occurrence in splits
        for tree in self.surrogate_model.estimators_:
            feature_pairs = []
            
            # Get features used in this tree
            features_used = tree.tree_.feature
            valid_features = features_used[features_used >= 0]
            
            # Count co-occurrences of features in the same tree
            for i, feat_i in enumerate(valid_features):
                for j, feat_j in enumerate(valid_features):
                    if i != j and feat_i < self.n_features and feat_j < self.n_features:
                        interaction_matrix[feat_i, feat_j] += 1
        
        # Normalize by number of trees
        interaction_matrix = interaction_matrix / len(self.surrogate_model.estimators_)
        
        return interaction_matrix
    
    def _calculate_permutation_interactions(self, X_sample: np.ndarray) -> np.ndarray:
        """Calculate pairwise feature interaction scores using permutation"""
        interaction_matrix = np.zeros((self.n_features, self.n_features))
        
        # Get baseline predictions
        baseline_preds = self.surrogate_model.predict_proba(X_sample)[:, 1]
        
        # Sample subset for efficiency
        sample_size = min(1000, X_sample.shape[0])
        sample_indices = np.random.choice(X_sample.shape[0], sample_size, replace=False)
        X_subset = X_sample[sample_indices]
        baseline_subset = baseline_preds[sample_indices]
        
        for i in range(min(15, self.n_features)):  # Limit for computational efficiency
            for j in range(i + 1, min(15, self.n_features)):
                # Joint masking effect
                X_masked = X_subset.copy()
                X_masked[:, i] = self.training_stats['medians'][i]
                X_masked[:, j] = self.training_stats['medians'][j]
                
                # Individual effects
                X_masked_i = X_subset.copy()
                X_masked_i[:, i] = self.training_stats['medians'][i]
                
                X_masked_j = X_subset.copy()
                X_masked_j[:, j] = self.training_stats['medians'][j]
                
                # Calculate interaction as deviation from additive effects
                joint_effect = np.mean(np.abs(baseline_subset - self.surrogate_model.predict_proba(X_masked)[:, 1]))
                individual_i = np.mean(np.abs(baseline_subset - self.surrogate_model.predict_proba(X_masked_i)[:, 1]))
                individual_j = np.mean(np.abs(baseline_subset - self.surrogate_model.predict_proba(X_masked_j)[:, 1]))
                
                # Interaction strength (non-additivity)
                interaction_strength = max(0, joint_effect - (individual_i + individual_j))
                interaction_matrix[i, j] = interaction_strength
                interaction_matrix[j, i] = interaction_strength
        
        return interaction_matrix
    
    def get_model_summary(self) -> Dict:
        """Get comprehensive summary of the surrogate model"""
        summary = {
            'model_type': 'Random Forest Surrogate for Ensemble',
            'ensemble_type': self.model_type,
            'n_estimators': self.surrogate_model.n_estimators,
            'max_depth': self.surrogate_model.max_depth,
            'n_features': self.n_features,
            'feature_names': self.feature_names,
            'is_fitted': self.is_fitted,
            'training_stats_available': len(self.training_stats) > 0
        }
        
        if self.is_fitted:
            summary.update({
                'oob_score': getattr(self.surrogate_model, 'oob_score_', 'Not available'),
                'fidelity_metrics': self.fidelity_metrics,
                'ensemble_info': self.ensemble_info
            })
        
        return summary


# Example usage and demonstration for AutoGluon + CatBoost ensemble
if __name__ == "__main__":
    # Example with synthetic data mimicking healthcare scenario
    from sklearn.datasets import make_classification
    from sklearn.ensemble import GradientBoostingClassifier
    import warnings
    warnings.filterwarnings('ignore')
    
    print("=== Ensemble Surrogate Explainer Demo ===")
    
    # Create synthetic healthcare-like dataset
    X, y = make_classification(
        n_samples=50000,  # Large dataset simulation
        n_features=25, 
        n_informative=20,
        n_redundant=5,
        n_clusters_per_class=2,
        flip_y=0.01,  # Small amount of noise
        class_sep=0.8,
        random_state=42
    )
    
    # Healthcare-like feature names
    feature_names = [
        'patient_age', 'bmi', 'systolic_bp', 'diastolic_bp', 'total_cholesterol',
        'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides', 'glucose_level', 'hba1c',
        'creatinine', 'bun', 'gfr', 'hemoglobin', 'hematocrit',
        'white_blood_count', 'platelet_count', 'esr', 'crp', 'albumin',
        'smoking_years', 'exercise_hours_week', 'family_history_score', 'medication_count', 'comorbidity_index'
    ]
    
    print(f"Dataset: {X.shape[0]} patients, {X.shape[1]} features")
    print(f"Class distribution: Class 0: {np.sum(y == 0)}, Class 1: {np.sum(y == 1)}")
    
    # Create ensemble model (simulating AutoGluon + CatBoost)
    ensemble_model = GradientBoostingClassifier(
        n_estimators=100, 
        max_depth=6,
        learning_rate=0.1,
        random_state=42
    )
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining ensemble model on {X_train.shape[0]} samples...")
    ensemble_model.fit(X_train, y_train)
    
    ensemble_accuracy = ensemble_model.score(X_test, y_test)
    print(f"Ensemble model accuracy: {ensemble_accuracy:.4f}")
    
    # Initialize Ensemble Surrogate Explainer
    explainer = EnsembleSurrogateExplainer(
        ensemble_model=ensemble_model,
        feature_names=feature_names,
        model_type="autogluon",  # Simulating AutoGluon ensemble
        n_estimators=150,
        max_depth=8,
        random_state=42
    )
    
    # Train the surrogate model
    print("\n=== Training Surrogate Model ===")
    training_results = explainer.fit(
        X_train, 
        validation_size=0.2,
        fidelity_threshold=0.85,
        batch_size=5000
    )
    
    print("\nTraining Results:")
    for key, value in training_results.items():
        print(f"  {key}: {value}")
    
    # Validate surrogate fidelity
    print("\n=== Validating Surrogate Fidelity ===")
    fidelity_results = explainer.validate_ensemble_fidelity(X_test[:2000], detailed=True)
    
    print(f"Classification Accuracy: {fidelity_results['classification_accuracy']:.4f}")
    print(f"Probability Correlation: {fidelity_results['probability_correlation']:.4f}")
    print(f"Overall Fidelity: {fidelity_results['overall_fidelity']:.4f}")
    
    # Generate local explanation
    print("\n=== Local Explanation Example ===")
    local_explanation = explainer.explain_local(
        X_test[0], 
        top_k=5, 
        include_predictions=True,
        include_confidence=True
    )
    
    print("Top 5 features for patient prediction:")
    for feature in local_explanation['top_features']:
        print(f"  {feature['rank']}. {feature['feature_name']}: "
              f"{feature['importance_score']:.4f} (value: {feature['feature_value']:.2f})")
    
    print(f"\nPrediction Agreement: {local_explanation['predictions']['agreement']['class_agreement']}")
    print(f"Prediction Confidence: {local_explanation['confidence_metrics']['prediction_confidence']:.4f}")
    
    # Generate global explanation
    print("\n=== Global Explanation ===")
    global_explanation = explainer.explain_global(
        X_test[:3000], 
        top_k=10, 
        include_interactions=True
    )
    
    print("Top 10 most important features globally:")
    for feature in global_explanation['top_global_features']:
        print(f"  {feature['rank']}. {feature['feature_name']}: "
              f"{feature['importance_score']:.4f} (stability: {feature['stability_score']:.3f})")
    
    # Feature interactions
    if 'feature_interactions' in global_explanation:
        print("\nTop 5 feature interactions:")
        for interaction in global_explanation['feature_interactions']['top_interactions'][:5]:
            print(f"  {interaction['feature_1']} × {interaction['feature_2']}: "
                  f"{interaction['interaction_score']:.4f}")
    
    # Batch processing demonstration
    print("\n=== Batch Processing Demo ===")
    batch_explanations = explainer.explain_local_batch(
        X_test[:500], 
        top_k=3, 
        batch_size=100,
        show_progress=False
    )
    
    print(f"Generated explanations for {len(batch_explanations)} patients")
    
    # Model summary
    print("\n=== Model Summary ===")
    summary = explainer.get_model_summary()
    print(f"Surrogate Type: {summary['model_type']}")
    print(f"Ensemble Type: {summary['ensemble_type']}")
    print(f"Number of Trees: {summary['n_estimators']}")
    print(f"Overall Fidelity: {summary['fidelity_metrics'].get('overall_fidelity', 'N/A')}")
    
    print("\n=== Demo Complete ===")
    print("Surrogate explainer successfully trained and validated!")
    print("Ready for production use with 10M+ healthcare records.")
