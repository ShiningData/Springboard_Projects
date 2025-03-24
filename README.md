# Springboard_Projects


## Introduction

This repository contains all the projects that were completed as part of Springboard's Data Science Career Track. However, it does not include the capstone and visualisation projects. They are available as separate repositories.


## Contents

Disclaimer: If you are a Springboard DSC Student, I strongly suggest you refrain from viewing the code before you've actually attempted at solving the problem yourself.

1. [Understanding Country Club Database with SQL - Manipulating data in SQL](http://localhost:8888/tree/Data_Science/Springboard_Projects/SQL_Project-Country_Club_Database)
2. [Analyzing World Bank Projects - Data Wrangling with JSON file](http://localhost:8888/tree/Data_Science/Springboard_Projects/Data_Wrangling_Project-JSON_File)
3. [API Project - Quandl - Data Wrangling](http://localhost:8888/tree/Data_Science/Springboard_Projects/API_Project-Quandl)
4. [What is the true Normal Human Body Temperature - Inferential Statistics](http://localhost:8888/tree/Data_Science/Springboard_Projects/Exploratory_Data_Analysis_Project-Normal_Human_Body_Temperature)
5. [Examining Racial Discrimination in the US Job Market - Inferential Statistics](http://localhost:8888/tree/Data_Science/Springboard_Projects/Exploratory_Data_Analysis_Project-Examine_Racial_Discrimination)
6. [Hospital Readmission Analysis and Recommendations - Inferential Statistics](http://localhost:8888/tree/Data_Science/Springboard_Projects/Exploratory_Data_Analysis_Project-Hospital_Readmissions)
7. [Predicting House Prices using Linear Regression - Supervised Machine Learning Project](http://localhost:8888/tree/Data_Science/Springboard_Projects/Linear_Regression_Project-Boston_Housing_Dataset)
8. [Predicting Gender using Logistic Regression - Supervised Machine Learning Project](http://localhost:8888/tree/Data_Science/Springboard_Projects/Logistic_Regression_Project-Gender_Classification_by_Heights_and_Weights)
9. [Movie Review Sentiment Analysis using Naive Bayes - Supervised Machine Learning Project](http://localhost:8888/tree/Data_Science/Springboard_Projects/Naive_Bayes_Project-Predicting_Movie_Ratings_From_Reviews)
10. [Wine Customer Segmentation using Unsupervised Learning - Unsupervised Machine Learning Project](http://localhost:8888/tree/Data_Science/Springboard_Projects/Clustering_Project-Customer_Segmentation)
11. [Spark Project-Databricks](http://localhost:8888/tree/Data_Science/Springboard_Projects/Spark_Project-Databricks)
12. [Ultimate Inc. Data Science Challenge - Time Series Project](http://localhost:8888/tree/Data_Science/Springboard_Projects/Take_Home_Challenge-Ultimate_Technologies_Inc)
13. [Relax Inc. Data Science Challenge](http://localhost:8888/tree/Data_Science/Springboard_Projects/Take_Home_Challenge-Relax_Inc)


Looking at your screenshot, I see you have a `feature_importance_dict` that contains condition names with their values and importance scores. Let me write a Python script to convert this data into a pandas DataFrame:

```python
import pandas as pd
import re

# Assuming feature_importance_dict is already defined and contains your data
# Based on your screenshot, I'll create a function to extract and organize this data

def convert_feature_importance_to_df(feature_importance_dict):
    # Create lists to store our extracted data
    all_conditions = []
    all_importances = []
    all_rule_indices = []
    
    # Iterate through the dictionary items
    for rule_idx, rule_data in feature_importance_dict.items():
        # Extract condition names and importances from each rule
        conditions = rule_data.get('conditions_names', [])
        importances = rule_data.get('scaled_importances', [])
        
        # Process each condition to extract just the feature name
        for i, condition in enumerate(conditions):
            # Extract feature name (everything before the equals sign)
            if isinstance(condition, str) and '=' in condition:
                feature_name = condition.split('=')[0].strip()
                
                # Add to our lists
                all_conditions.append(feature_name)
                
                # Get the corresponding importance value if available
                importance_val = importances[i] if i < len(importances) else None
                all_importances.append(importance_val)
                
                # Keep track of which rule this belongs to
                all_rule_indices.append(rule_idx)
    
    # Create a DataFrame from our collected data
    df = pd.DataFrame({
        'rule_index': all_rule_indices,
        'feature': all_conditions,
        'importance': all_importances
    })
    
    return df

# Call the function to convert the dictionary to a DataFrame
feature_importance_df = convert_feature_importance_to_df(feature_importance_dict)

# Display the DataFrame
print(feature_importance_df)

# You might want to further process this data, such as:
# - Get the average importance per feature across all rules
avg_importance_by_feature = feature_importance_df.groupby('feature')['importance'].mean().reset_index()
avg_importance_by_feature = avg_importance_by_feature.sort_values('importance', ascending=False)

print("\nAverage Importance by Feature:")
print(avg_importance_by_feature)

# - Get unique features used in rules
unique_features = feature_importance_df['feature'].unique()
print("\nUnique Features:")
print(unique_features)
```

If your `feature_importance_dict` has a different structure than what I've assumed, you might need to adjust the extraction logic. Looking at your screenshot, it appears the dict items contain tuples with feature names and values, followed by importance scores. Here's an alternative approach if the structure is different:

```python
import pandas as pd

# Alternative approach if the structure is different
def process_feature_importance_dict(feature_importance_dict):
    data = []
    
    for rule_idx, rule_info in feature_importance_dict.items():
        # Assuming rule_info is a tuple with conditions and importances
        for item in rule_info:
            if isinstance(item, list) and len(item) > 0:
                for i, condition in enumerate(item):
                    if isinstance(condition, str) and '=' in condition:
                        feature_name = condition.split('=')[0].strip()
                        value_part = condition.split('=')[1].strip()
                        importance = None
                        
                        # Find corresponding importance if available
                        if i < len(item) - 1 and isinstance(item[i+1], (int, float)):
                            importance = item[i+1]
                        
                        data.append({
                            'rule_index': rule_idx,
                            'feature': feature_name,
                            'value': value_part,
                            'importance': importance
                        })
    
    return pd.DataFrame(data)

# Create the DataFrame
feature_df = process_feature_importance_dict(feature_importance_dict)
print(feature_df)
```

Based on the exact structure of your `feature_importance_dict`, you might need to combine or modify these approaches. If you share more details about the exact format, I can provide a more accurate solution.
