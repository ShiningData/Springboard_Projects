import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
from sklearn.utils.class_weight import compute_class_weight, compute_sample_weight

# Load your data
# train_df = pd.read_csv('your_data.csv')

# Calculate class weights
classes = train_df['carcode'].unique()
class_weights = compute_class_weight('balanced', classes=classes, y=train_df['carcode'])
class_weight_dict = {classes[i]: class_weights[i] for i in range(len(classes))}

# Create sample weights for each row
sample_weights = compute_sample_weight('balanced', train_df['carcode'])

# Train with AutoGluon
predictor = TabularPredictor(
    label='carcode',
    problem_type='multiclass',
    eval_metric='balanced_accuracy'
)

# Option 1: Using focal loss
predictor.fit(
    train_data=train_df,
    hyperparameters={
        "optimization.loss_function": "focal_loss",
        "optimization.focal_loss.gamma": 2.0,  # Adjust based on your data
        "optimization.focal_loss.alpha": class_weight_dict,
        "optimization.max_epochs": 100
    },
    time_limit=3600  # Adjust based on your computational resources
)

# Evaluate
predictor.evaluate(test_df)
