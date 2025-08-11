def get_top_k_features_and_values(shap_values, feature_names, top_k=5):
    # Get top k indices by absolute values
    top_k_indices = np.argsort(np.absolute(shap_values), axis=1)[:, -top_k:][:, ::-1]
    
    # Get corresponding SHAP values
    top_k_values = np.take_along_axis(shap_values, top_k_indices, axis=1)
    
    # Convert indices to feature names
    top_k_names = []
    for sample_indices in top_k_indices:
        top_k_names.append([feature_names[i] for i in sample_indices])
    
    return np.array(top_k_names), top_k_values

# Usage
top_5_features, top_5_values = get_top_k_features_and_values(shap_values, feature_names, 5)

# Example: Top 5 for sample 0
print("Features:", top_5_features[0])
print("SHAP values:", top_5_values[0])

===================

def get_top_features_structured(shap_values, feature_names, top_k=5):
    top_k_indices = np.argsort(np.absolute(shap_values), axis=1)[:, -top_k:][:, ::-1]
    top_k_values = np.take_along_axis(shap_values, top_k_indices, axis=1)
    
    # Create feature names array
    top_k_names = np.array([[feature_names[i] for i in sample_indices] 
                           for sample_indices in top_k_indices])
    
    return {
        'features': top_k_names,           # Shape: (n_samples, top_k)
        'shap_values': top_k_values,       # Shape: (n_samples, top_k)
        'indices': top_k_indices,          # Shape: (n_samples, top_k)
        'abs_values': np.absolute(top_k_values)  # Shape: (n_samples, top_k)
    }

# Usage
result = get_top_features_structured(shap_values, feature_names, 5)

# Access for specific sample
sample_idx = 0
print(f"Top 5 features for sample {sample_idx}:")
for i in range(5):
    feature = result['features'][sample_idx, i]
    value = result['shap_values'][sample_idx, i]
    print(f"  {i+1}. {feature}: {value:.4f}")
