import numpy as np
from typing import Dict, List, Optional
import warnings

class EnterpriseSafeExplainer:
    """
    AGPL-free local explainability for AutoGluon + CatBoost ensemble
    No null value imputation - uses masking strategies only
    """
    
    def __init__(self, autogluon_model, feature_names: List[str]):
        self.autogluon_model = autogluon_model
        self.feature_names = feature_names
        self.catboost_models = self._extract_catboost_models()
        self.background_stats = {}
    
    def fit(self, X_background: np.ndarray):
        """Calculate background statistics (no imputation, just for masking)"""
        self.background_stats = {
            'medians': np.nanmedian(X_background, axis=0),
            'means': np.nanmean(X_background, axis=0),
            'zeros': np.zeros(X_background.shape[1])
        }
    
    def explain_local(self, instance: np.ndarray, top_k: int = 5) -> Dict:
        """
        Generate local explanations using both model-agnostic and tree-based methods
        NO NULL VALUE IMPUTATION
        """
        explanation = {
            'instance_prediction': self.autogluon_model.predict_proba(instance.reshape(1, -1))[0],
            'model_agnostic_importance': self._model_agnostic_explanation(instance),
            'tree_based_importance': self._tree_based_explanation(instance),
            'consensus_importance': None,
            'top_features': []
        }
        
        # Calculate consensus
        consensus = self._calculate_consensus(
            explanation['model_agnostic_importance'],
            explanation['tree_based_importance']
        )
        explanation['consensus_importance'] = consensus
        
        # Get top k features
        if consensus is not None:
            top_indices = np.argsort(consensus)[::-1][:top_k]
            explanation['top_features'] = [
                {
                    'feature_name': self.feature_names[idx],
                    'importance': consensus[idx],
                    'value': instance[idx]
                }
                for idx in top_indices
            ]
        
        return explanation
    
    def _model_agnostic_explanation(self, instance: np.ndarray) -> np.ndarray:
        """Model-agnostic permutation importance with masking (no imputation)"""
        baseline_prob = self.autogluon_model.predict_proba(instance.reshape(1, -1))[0, 1]
        importance_scores = np.zeros(len(instance))
        
        for feature_idx in range(len(instance)):
            # Strategy 1: Zero masking
            masked_instance = instance.copy()
            masked_instance[feature_idx] = 0
            masked_prob = self.autogluon_model.predict_proba(masked_instance.reshape(1, -1))[0, 1]
            zero_importance = abs(baseline_prob - masked_prob)
            
            # Strategy 2: Median masking (no imputation, just background reference)
            masked_instance = instance.copy()
            masked_instance[feature_idx] = self.background_stats['medians'][feature_idx]
            median_masked_prob = self.autogluon_model.predict_proba(masked_instance.reshape(1, -1))[0, 1]
            median_importance = abs(baseline_prob - median_masked_prob)
            
            # Average the strategies
            importance_scores[feature_idx] = (zero_importance + median_importance) / 2
        
        return importance_scores
    
    def _tree_based_explanation(self, instance: np.ndarray) -> Optional[np.ndarray]:
        """Tree-based explanations using TreeInterpreter and CatBoost native methods"""
        if not self.catboost_models:
            return None
        
        all_contributions = []
        
        for model_name, catboost_model in self.catboost_models.items():
            try:
                # Use CatBoost's native feature importance (no imputation needed)
                from catboost import Pool
                pool = Pool(instance.reshape(1, -1))
                contributions = catboost_model.get_feature_importance(
                    pool, type='PredictionValuesChange'
                )[0]  # Get first (and only) instance
                
                all_contributions.append(np.abs(contributions))
                
            except Exception as e:
                warnings.warn(f"Could not get contributions from {model_name}: {e}")
                continue
        
        if all_contributions:
            # Average across all CatBoost models
            return np.mean(all_contributions, axis=0)
        
        return None
    
    def _extract_catboost_models(self) -> Dict:
        """Extract CatBoost models from AutoGluon ensemble"""
        catboost_models = {}
        
        try:
            if hasattr(self.autogluon_model, '_trainer'):
                models_dict = self.autogluon_model._trainer.model_best.models
                
                for model_name, model_obj in models_dict.items():
                    if 'catboost' in model_obj.__class__.__name__.lower():
                        catboost_models[model_name] = getattr(model_obj, 'model', model_obj)
                        
        except Exception as e:
            warnings.warn(f"Could not extract CatBoost models: {e}")
        
        return catboost_models
    
    def _calculate_consensus(self, agnostic_importance: np.ndarray, 
                           tree_importance: Optional[np.ndarray]) -> Optional[np.ndarray]:
        """Calculate consensus between model-agnostic and tree-based importance"""
        if tree_importance is None:
            return agnostic_importance
        
        if agnostic_importance is None:
            return tree_importance
        
        # Normalize both to [0, 1] range
        agnostic_norm = agnostic_importance / np.max(agnostic_importance) if np.max(agnostic_importance) > 0 else agnostic_importance
        tree_norm = tree_importance / np.max(tree_importance) if np.max(tree_importance) > 0 else tree_importance
        
        # Weighted average (slightly favor tree-based for interpretability)
        consensus = 0.4 * agnostic_norm + 0.6 * tree_norm
        
        return consensus
    
    def batch_explain(self, X_batch: np.ndarray, batch_size: int = 1000) -> List[Dict]:
        """Efficiently explain large batches (for your 10M records)"""
        explanations = []
        
        for i in range(0, len(X_batch), batch_size):
            batch = X_batch[i:i + batch_size]
            
            for instance in batch:
                explanation = self.explain_local(instance)
                explanations.append(explanation)
        
        return explanations
