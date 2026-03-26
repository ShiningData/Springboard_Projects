# End-to-End Classification Modeling — Customer Churn

A hands-on workshop repository that walks you through every stage of a
binary-classification project: from raw data to a production-ready model you
can score single records or entire datasets with.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Prerequisites](#prerequisites)
3. [Environment Setup](#environment-setup)
4. [Understanding the Data](#understanding-the-data)
5. [Pipeline Overview](#pipeline-overview)
6. [Option A — Interactive Notebook](#option-a--interactive-notebook)
7. [Option B — Command-Line Training](#option-b--command-line-training)
8. [Running Inference](#running-inference)
9. [Source Modules Reference](#source-modules-reference)
10. [Key Concepts Covered](#key-concepts-covered)

---

## Project Structure

```
classification-modeling/
├── data/
│   ├── raw/                 # Original churn.csv (input)
│   └── processed/           # Scored predictions (output)
├── notebooks/
│   └── churn_classification_pipeline.ipynb   # Step-by-step walkthrough
├── models/
│   └── best_model.joblib    # Saved pipeline (after training)
├── src/
│   ├── main.py              # End-to-end training script
│   ├── inference.py         # Single-record & batch prediction CLI
│   ├── ingestion.py         # Repeatable CSV loading
│   ├── validation.py        # Data-quality checks
│   ├── preprocessing.py     # ColumnTransformer builder
│   ├── features.py          # Splitting & feature-name helpers
│   ├── train.py             # Baseline, model zoo, hyperparameter tuning
│   └── evaluate.py          # Metrics, PR curve, comparison tables
├── requirements.txt
└── README.md
```

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.10.x |
| Conda (Anaconda / Miniconda) | any recent version |
| Git | any recent version |

---

## Environment Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd classification-modeling
```

### 2. Create the conda environment

```bash
conda create -n churn python=3.10.16 -y
conda activate churn
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Register the Jupyter kernel (for notebook use)

```bash
python -m ipykernel install --user --name churn --display-name "Python 3.10 (churn)"
```

You are now ready to run either the notebook or the CLI.

---

## Understanding the Data

The dataset (`data/raw/churn.csv`) contains ~165 K bank customers with the
following features:

| Column | Type | Description |
|--------|------|-------------|
| CreditScore | numeric | Customer's credit score |
| Geography | categorical | Country (France, Germany, Spain) |
| Gender | categorical | Male / Female |
| Age | numeric | Customer's age |
| Tenure | numeric | Years with the bank |
| Balance | numeric | Account balance |
| NumOfProducts | numeric | Number of bank products used |
| HasCrCard | binary | Has a credit card (1/0) |
| IsActiveMember | binary | Active member (1/0) |
| EstimatedSalary | numeric | Estimated annual salary |
| **Exited** | **target** | **1 = churned, 0 = stayed** |

The target is **imbalanced** (~20 % positive class), which is a core theme of
this workshop.

---

## Pipeline Overview

The full pipeline runs through these stages:

```
 ┌─────────┐    ┌────────────┐    ┌────────────────┐    ┌──────────┐
 │ Ingest  │───▶│  Validate  │───▶│  Preprocess &  │───▶│  Split   │
 │  CSV    │    │  quality   │    │  feature eng.  │    │ 60/20/20 │
 └─────────┘    └────────────┘    └────────────────┘    └────┬─────┘
                                                             │
     ┌───────────────────────────────────────────────────────┘
     ▼
 ┌──────────┐    ┌───────────┐    ┌──────────┐    ┌──────────┐
 │ Baseline │───▶│ Model Zoo │───▶│  Tune    │───▶│ Evaluate │
 │ LogReg   │    │ RF/GB/XGB │    │ best one │    │ on Test  │
 └──────────┘    └───────────┘    └──────────┘    └────┬─────┘
                                                       │
     ┌─────────────────────────────────────────────────┘
     ▼
 ┌───────────────┐    ┌─────────────────────┐
 │ Save pipeline │───▶│ Inference (single / │
 │ to .joblib    │    │ batch prediction)   │
 └───────────────┘    └─────────────────────┘
```

---

## Option A — Interactive Notebook

Best for learning. Each section has markdown notes explaining **what** is done
and **why**.

```bash
conda activate churn
jupyter notebook notebooks/churn_classification_pipeline.ipynb
```

Select the **Python 3.10 (churn)** kernel when prompted.

The notebook covers 12 sections:

| # | Section | What You'll Learn |
|---|---------|-------------------|
| 1 | Project Setup | Folder layout, imports, environment check |
| 2 | Ingestion & Validation | `load_data()`, `validate_data()` — repeatable loading & quality gates |
| 3 | EDA | Target imbalance, feature distributions, leakage check |
| 4 | Preprocessing Pipeline | `ColumnTransformer` — imputation, scaling, one-hot encoding |
| 5 | Train / Val / Test Split | 60/20/20 stratified split — why three sets matter |
| 6 | Baseline & Metrics | Logistic Regression + choosing Recall/F1 as primary metric |
| 7 | Imbalance Handling Lab | Class weights vs threshold tuning vs SMOTE — comparison table |
| 8 | PCA Mini-Lab | Explained variance, PCA vs non-PCA trade-off |
| 9 | Model Zoo | Random Forest, Gradient Boosting, XGBoost with `scale_pos_weight` |
| 10 | Hyperparameter Tuning | `RandomizedSearchCV` on validation (never on test) |
| 11 | Evaluation & Interpretability | Test-set metrics, feature importance (gain-based) |
| 12 | Save & Predict | `best_model.joblib` + `predict_one()` demo |

---

## Option B — Command-Line Training

Run the full pipeline as a single script — same steps as the notebook but
automated.

```bash
conda activate churn

# Default (uses data/raw/churn.csv, 20 tuning iterations):
python src/main.py

# Custom options:
python src/main.py --data data/raw/churn.csv --n-iter 30

# Quick run (skip hyperparameter tuning):
python src/main.py --skip-tuning
```

**What it does:**

1. Loads and validates `data/raw/churn.csv`
2. Splits data 60/20/20 (stratified)
3. Trains a Logistic Regression baseline
4. Trains a weighted Logistic Regression
5. Trains Random Forest, Gradient Boosting, and XGBoost
6. Tunes the best model with `RandomizedSearchCV`
7. Prints a validation comparison table
8. Evaluates the final model on the held-out test set
9. Saves the pipeline to `models/best_model.joblib`

---

## Running Inference

After training, use `inference.py` to make predictions.

### Single-Record Prediction

Predict churn for one customer by passing feature values as arguments:

```bash
python src/inference.py single \
    --creditscore 650 \
    --geography France \
    --gender Female \
    --age 45 \
    --tenure 3 \
    --balance 125000 \
    --numofproducts 1 \
    --hascrcard 1 \
    --isactivemember 0 \
    --estimatedsalary 80000
```

Output:

```
Model loaded ← models/best_model.joblib

  Churn probability : 0.6234
  Prediction        : CHURN
```

### Batch Dataset Prediction

Score every row in a CSV and save results:

```bash
python src/inference.py batch \
    --input data/raw/churn.csv \
    --output data/processed/predictions.csv
```

The output CSV will contain all original columns plus:
- `churn_probability` — model confidence (0.0 – 1.0)
- `churn_prediction` — binary label (1 = churn)

You can also set a custom decision threshold:

```bash
python src/inference.py batch \
    --input data/raw/churn.csv \
    --output data/processed/predictions.csv \
    --threshold 0.3
```

### Using Inference in Python

```python
from inference import load_model, predict_one, predict_dataset

model = load_model("models/best_model.joblib")

# Single record
result = predict_one(
    {"creditscore": 650, "geography": "France", "gender": "Female",
     "age": 45, "tenure": 3, "balance": 125000.0, "numofproducts": 1,
     "hascrcard": 1.0, "isactivemember": 0.0, "estimatedsalary": 80000.0},
    model=model,
)
print(result)
# {'churn_probability': 0.6234, 'prediction': 1}

# Batch dataset
df_scored = predict_dataset(
    "data/raw/churn.csv", model=model,
    output_path="data/processed/predictions.csv",
)
```

---

## Source Modules Reference

Each module in `src/` encapsulates one responsibility:

| Module | Key Functions | Purpose |
|--------|---------------|---------|
| `ingestion.py` | `load_data(path)` | Read CSV, normalize columns, drop IDs |
| `validation.py` | `validate_data(df)` | Check columns, target integrity, missing rates, duplicates, ranges |
| `preprocessing.py` | `build_preprocessor(num, cat)`, `get_feature_lists(df)` | Build `ColumnTransformer` (impute + scale + OHE) |
| `features.py` | `split_data(df)`, `get_feature_names_from_pipeline(pipe)` | Stratified 3-way split, post-OHE feature names |
| `train.py` | `train_baseline()`, `train_model_zoo()`, `tune_xgboost()` | Train LogReg, RF, GBM, XGBoost; hyperparameter search |
| `evaluate.py` | `evaluate_model()`, `sweep_thresholds()`, `compare_models()` | Metrics report, PR curve, threshold sweep, comparison table |
| `inference.py` | `predict_one()`, `predict_dataset()`, `save_model()`, `load_model()` | Persist model, single & batch prediction |
| `main.py` | `main()` | Orchestrate the full training pipeline end-to-end |

---

## Key Concepts Covered

- **Imbalanced classification** — why accuracy is misleading and how to use Recall, F1, PR-AUC instead
- **Class weights** — `class_weight='balanced'` shifts the loss function toward the minority class
- **Threshold tuning** — adjusting the decision boundary on the validation set
- **SMOTE** — synthetic oversampling inside the pipeline (not before split!) to avoid leakage
- **PCA** — dimensionality reduction trade-off: performance vs interpretability
- **Ensemble methods** — bagging (Random Forest) vs boosting (Gradient Boosting, XGBoost)
- **`scale_pos_weight`** — XGBoost's built-in imbalance knob (≈ negative/positive ratio)
- **Hyperparameter tuning** — `RandomizedSearchCV` on validation folds, never on the test set
- **Feature importance** — gain-based importance; importance ≠ causality
- **Pipeline discipline** — `ColumnTransformer` inside `Pipeline` ensures identical transforms in training and inference
