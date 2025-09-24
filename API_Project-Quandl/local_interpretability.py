import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# Install required packages (run these in terminal/notebook):
# pip install lime shap

import lime
import lime.lime_tabular
import shap

# Set random seed for reproducibility
np.random.seed(42)

class LocalExplainabilityDemo:
    def __init__(self):
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None
        self.scaler = StandardScaler()
        
    def load_and_prepare_data(self):
        """Load and prepare the breast cancer dataset"""
        # Load dataset
        data = load_breast_cancer()
        X, y = data.data, data.target
        self.feature_names = data.feature_names
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        self.X_train = self.scaler.fit_transform(X_train)
        self.X_test = self.scaler.transform(X_test)
        self.y_train = y_train
        self.y_test = y_test
        
        print(f"Dataset shape: {X.shape}")
        print(f"Training set: {self.X_train.shape}, Test set: {self.X_test.shape}")
        print(f"Classes: {data.target_names}")
        
    def train_model(self):
        """Train a Random Forest classifier"""
        self.model = RandomForestClassifier(
            n_estimators=100, 
            random_state=42,
            max_depth=10
        )
        
        self.model.fit(self.X_train, self.y_train)
        
        # Evaluate model
        y_pred = self.model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        print(f"\nModel Accuracy: {accuracy:.3f}")
        
    def explain_with_lime(self, instance_idx=0):
        """Explain a single prediction using LIME"""
        print(f"\n{'='*50}")
        print("LIME EXPLANATION")
        print(f"{'='*50}")
        
        # Create LIME explainer
        explainer = lime.lime_tabular.LimeTabularExplainer(
            self.X_train,
            feature_names=self.feature_names,
            class_names=['Malignant', 'Benign'],
            mode='classification'
        )
        
        # Select instance to explain
        instance = self.X_test[instance_idx]
        
        # Generate explanation
        explanation = explainer.explain_instance(
            instance, 
            self.model.predict_proba,
            num_features=10
        )
        
        # Print explanation
        print(f"Explaining instance {instance_idx}")
        print(f"True label: {'Benign' if self.y_test[instance_idx] == 1 else 'Malignant'}")
        print(f"Predicted label: {'Benign' if self.model.predict([instance])[0] == 1 else 'Malignant'}")
        print(f"Prediction probability: {self.model.predict_proba([instance])[0]}")
        
        print("\nTop 10 most important features:")
        for feature, importance in explanation.as_list():
            print(f"  {feature}: {importance:.3f}")
            
        # Save explanation as HTML (optional)
        explanation.save_to_file(f'lime_explanation_instance_{instance_idx}.html')
        print(f"\nDetailed explanation saved to lime_explanation_instance_{instance_idx}.html")
        
        return explanation
        
    def explain_with_shap(self, num_instances=5):
        """Explain predictions using SHAP"""
        print(f"\n{'='*50}")
        print("SHAP EXPLANATION")
        print(f"{'='*50}")
        
        # Create SHAP explainer
        explainer = shap.TreeExplainer(self.model)
        
        # Calculate SHAP values for a subset of test data
        shap_values = explainer.shap_values(self.X_test[:num_instances])
        
        # For binary classification, SHAP returns values for both classes
        # We'll use the positive class (Benign = 1)
        shap_values_positive = shap_values[1] if len(shap_values) == 2 else shap_values
        
        print(f"Calculated SHAP values for {num_instances} instances")
        print(f"Shape of SHAP values: {shap_values_positive.shape}")
        
        # Summary plot
        plt.figure(figsize=(10, 6))
        shap.summary_plot(
            shap_values_positive, 
            self.X_test[:num_instances], 
            feature_names=self.feature_names,
            show=False
        )
        plt.title("SHAP Summary Plot")
        plt.tight_layout()
        plt.savefig('shap_summary_plot.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Waterfall plot for first instance
        plt.figure(figsize=(10, 8))
        shap.waterfall_plot(
            explainer.expected_value[1], 
            shap_values_positive[0], 
            self.X_test[0], 
            feature_names=self.feature_names,
            show=False
        )
        plt.title("SHAP Waterfall Plot - Instance 0")
        plt.tight_layout()
        plt.savefig('shap_waterfall_plot.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return shap_values_positive
        
    def compare_explanations(self, instance_idx=0):
        """Compare LIME and SHAP explanations for the same instance"""
        print(f"\n{'='*50}")
        print("COMPARING LIME vs SHAP")
        print(f"{'='*50}")
        
        # LIME explanation
        lime_explainer = lime.lime_tabular.LimeTabularExplainer(
            self.X_train,
            feature_names=self.feature_names,
            class_names=['Malignant', 'Benign'],
            mode='classification'
        )
        
        lime_explanation = lime_explainer.explain_instance(
            self.X_test[instance_idx], 
            self.model.predict_proba,
            num_features=10
        )
        
        # SHAP explanation
        shap_explainer = shap.TreeExplainer(self.model)
        shap_values = shap_explainer.shap_values(self.X_test[instance_idx:instance_idx+1])
        shap_values_positive = shap_values[1][0] if len(shap_values) == 2 else shap_values[0]
        
        # Create comparison dataframe
        lime_dict = dict(lime_explanation.as_list())
        
        comparison_data = []
        for i, feature_name in enumerate(self.feature_names):
            lime_importance = lime_dict.get(feature_name, 0)
            shap_importance = shap_values_positive[i]
            
            comparison_data.append({
                'Feature': feature_name,
                'LIME_Importance': lime_importance,
                'SHAP_Importance': shap_importance,
                'Feature_Value': self.X_test[instance_idx][i]
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Sort by absolute SHAP importance
        comparison_df['abs_shap'] = abs(comparison_df['SHAP_Importance'])
        comparison_df = comparison_df.sort_values('abs_shap', ascending=False)
        
        print(f"\nTop 10 features comparison for instance {instance_idx}:")
        print(comparison_df[['Feature', 'LIME_Importance', 'SHAP_Importance', 'Feature_Value']].head(10).to_string(index=False))
        
        # Visualization
        top_features = comparison_df.head(10)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
        
        # LIME importance
        ax1.barh(range(len(top_features)), top_features['LIME_Importance'])
        ax1.set_yticks(range(len(top_features)))
        ax1.set_yticklabels([f.replace('mean ', '') for f in top_features['Feature']], fontsize=8)
        ax1.set_xlabel('LIME Importance')
        ax1.set_title('LIME Feature Importance')
        ax1.grid(True, alpha=0.3)
        
        # SHAP importance
        ax2.barh(range(len(top_features)), top_features['SHAP_Importance'])
        ax2.set_yticks(range(len(top_features)))
        ax2.set_yticklabels([f.replace('mean ', '') for f in top_features['Feature']], fontsize=8)
        ax2.set_xlabel('SHAP Importance')
        ax2.set_title('SHAP Feature Importance')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('lime_vs_shap_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return comparison_df
        
    def global_feature_importance(self):
        """Show global feature importance from the model"""
        print(f"\n{'='*50}")
        print("GLOBAL FEATURE IMPORTANCE")
        print(f"{'='*50}")
        
        # Get feature importance from the model
        importance_df = pd.DataFrame({
            'Feature': self.feature_names,
            'Importance': self.model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        print("Top 10 most important features globally:")
        print(importance_df.head(10).to_string(index=False))
        
        # Plot
        plt.figure(figsize=(10, 8))
        top_10_features = importance_df.head(10)
        plt.barh(range(len(top_10_features)), top_10_features['Importance'])
        plt.yticks(range(len(top_10_features)), 
                  [f.replace('mean ', '') for f in top_10_features['Feature']])
        plt.xlabel('Feature Importance')
        plt.title('Global Feature Importance (Random Forest)')
        plt.gca().invert_yaxis()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('global_feature_importance.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return importance_df

def main():
    """Main function to run the explainability demo"""
    print("Local Model Explainability Demo")
    print("=" * 50)
    
    # Initialize demo
    demo = LocalExplainabilityDemo()
    
    # Load and prepare data
    demo.load_and_prepare_data()
    
    # Train model
    demo.train_model()
    
    # Global importance
    demo.global_feature_importance()
    
    # LIME explanation for first test instance
    lime_exp = demo.explain_with_lime(instance_idx=0)
    
    # SHAP explanations
    shap_values = demo.explain_with_shap(num_instances=5)
    
    # Compare explanations
    comparison = demo.compare_explanations(instance_idx=0)
    
    print(f"\n{'='*50}")
    print("DEMO COMPLETED")
    print(f"{'='*50}")
    print("Files generated:")
    print("- lime_explanation_instance_0.html")
    print("- shap_summary_plot.png")
    print("- shap_waterfall_plot.png")
    print("- lime_vs_shap_comparison.png")
    print("- global_feature_importance.png")

if __name__ == "__main__":
    main()
