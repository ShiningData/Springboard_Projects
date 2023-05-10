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







import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from jupyter_dash import JupyterDash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

# Load data
wire_segment = pd.DataFrame({
    'segment': ['A', 'B', 'C', 'D', 'E'],
    'tran_direction': ['Inbound', 'Outbound', 'Outbound', 'Inbound', 'Outbound'],
    'total_tran_count': [500, 300, 200, 700, 400],
    'total_tran_amt': [100000, 50000, 30000, 120000, 80000]
})

# Define app
app = JupyterDash(__name__)

# Define direction dropdown options
directions = wire_segment['tran_direction'].unique()

# Define app layout
app.layout = html.Div(children=[
    html.H1(children='Wire Segments Table'),
    
    dcc.Dropdown(
        id='direction_dropdown',
        options=[{'label': i, 'value': i} for i in directions],
        value=directions[0]
    ),
    
    dcc.Graph(
        id='table'
    )
])

# Define make_table function
def make_table(df, direction):
    # filter data based on direction
    filtered_df = df[df['tran_direction'] == direction]
    
    # sort data based on total_tran_amt in descending order
    sorted_df = filtered_df.sort_values(['total_tran_amt'], ascending=False)
    
    # create table using plotly
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(sorted_df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[sorted_df.segment, sorted_df.tran_direction,
                           sorted_df.total_tran_count, sorted_df.total_tran_amt],
                   fill_color='lavender',
                   align='left'))
    ])
    
    return fig

# Define update_table callback function
@app.callback(Output('table', 'figure'),
              [Input('direction_dropdown', 'value')])
def update_table(direction):
    fig = make_table(wire_segment, direction)
    return fig

# Run app
app.run_server(mode='inline')
