import pandas as pd
import yaml

def load_yaml_rules(yaml_path):
    """Load the YAML rules from a file."""
    with open(yaml_path, 'r') as f:
        rules = yaml.safe_load(f)
    return rules

def get_always_mandatory_columns(rules):
    """Extract always mandatory columns from YAML rules."""
    return rules.get('always_mandatory', [])

def get_conditional_mandatory_columns(rules, row):
    """
    Given a row, return a list of conditional mandatory columns that apply.
    """
    conditional_columns = []
    for condition in rules.get('conditional_mandatory', []):
        cond = condition['condition']
        col = cond['column']
        val = cond['value']
        if row.get(col) == val:
            conditional_columns.extend(condition['required_columns'])
    return conditional_columns

def split_data_by_mandatory_columns(df, yaml_path):
    """
    Splits the DataFrame into missing_data and complete_data based on YAML rules.
    Returns (missing_data, complete_data)
    """
    rules = load_yaml_rules(yaml_path)
    always_mandatory = get_always_mandatory_columns(rules)
    # Columns that must be positive
    positive_columns = ['age', 'amount']

    missing_rows = []
    complete_rows = []

    for idx, row in df.iterrows():
        missing = False
        # Check always mandatory columns for missing or empty
        for col in always_mandatory:
            if pd.isnull(row.get(col)) or row.get(col) == '':
                missing = True
                break
        # Check positivity for specific columns if present
        if not missing:
            for pos_col in positive_columns:
                if pos_col in always_mandatory:
                    value = row.get(pos_col)
                    if pd.isnull(value) or value == '' or value <= 0:
                        missing = True
                        break
        # Check conditional mandatory columns
        if not missing:
            cond_cols = get_conditional_mandatory_columns(rules, row)
            for col in cond_cols:
                if pd.isnull(row.get(col)) or row.get(col) == '':
                    missing = True
                    break

        if missing:
            missing_rows.append(idx)
        else:
            complete_rows.append(idx)

    missing_data = df.loc[missing_rows].copy()
    complete_data = df.loc[complete_rows].copy()
    return missing_data, complete_data
