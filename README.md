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




import pandas as pd
import json
from typing import Dict, List, Any, Union

def expand_nested_json(data: Union[List[Dict], Dict], separator: str = "_") -> pd.DataFrame:

    # If input is a dictionary, convert to a list containing that dictionary
    if isinstance(data, dict):
        data = [data]
    
    # If input is a string (JSON), parse it
    if isinstance(data, str):
        data = json.loads(data)
        if isinstance(data, dict):
            data = [data]
    
    # First convert to DataFrame
    df = pd.DataFrame(data)
    
    # Function to flatten nested columns
    def flatten_nested_columns(df: pd.DataFrame, separator: str = "_") -> pd.DataFrame:
        # Create a copy to avoid modifying the original DataFrame
        result_df = df.copy()
        
        # Find columns with dictionaries or lists
        nested_columns = [
            col for col in result_df.columns
            if any(isinstance(val, (dict, list)) for val in result_df[col].dropna())
        ]
        
        # No nested columns to expand
        if not nested_columns:
            return result_df
            
        # Process each nested column
        for col in nested_columns:
            # Handle dictionary columns
            if any(isinstance(val, dict) for val in result_df[col].dropna()):
                # Convert column to DataFrame
                expanded = pd.json_normalize(
                    result_df[col].apply(lambda x: {} if pd.isna(x) else x)
                )
                
                # Rename columns with prefix
                expanded.columns = [f"{col}{separator}{subcol}" for subcol in expanded.columns]
                
                # Drop the original column and join with expanded columns
                result_df = result_df.drop(col, axis=1).join(expanded)
            
            # Handle list columns
            elif any(isinstance(val, list) for val in result_df[col].dropna()):
                # Handle lists of dictionaries
                if any(isinstance(item, dict) for sublist in result_df[col].dropna() for item in sublist if sublist):
                    # Create a temporary column with the index
                    result_df['_temp_idx'] = range(len(result_df))
                    
                    # Explode the list column into separate rows
                    exploded = result_df[[col, '_temp_idx']].explode(col)
                    
                    # Normalize the exploded dictionaries
                    if not exploded.empty and any(isinstance(val, dict) for val in exploded[col].dropna()):
                        expanded = pd.json_normalize(
                            exploded[col].apply(lambda x: {} if pd.isna(x) else x)
                        )
                        
                        # Prefix column names
                        expanded.columns = [f"{col}{separator}{subcol}" for subcol in expanded.columns]
                        
                        # Join with the index column
                        expanded['_temp_idx'] = exploded['_temp_idx'].values
                        
                        # Group by index and convert expanded columns to lists
                        grouped = expanded.groupby('_temp_idx').agg(list)
                        
                        # Join with the original DataFrame
                        result_df = result_df.drop(col, axis=1).join(grouped, on='_temp_idx')
                    
                    # Clean up temporary index column
                    result_df = result_df.drop('_temp_idx', axis=1)
                
                # Handle simple lists (strings, numbers)
                else:
                    # Convert lists to strings for simple representation
                    result_df[col] = result_df[col].apply(
                        lambda x: json.dumps(x) if isinstance(x, list) else x
                    )
        
        # Recursively process any new nested columns that were created
        return flatten_nested_columns(result_df, separator)
    
    # Apply the recursive flattening
    flattened_df = flatten_nested_columns(df, separator)
    
    return flattened_df
