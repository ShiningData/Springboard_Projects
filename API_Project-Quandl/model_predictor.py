import pandas as pd
import yaml
import math

def is_valid_value(value):
    """
    Check if a value is valid (not missing, empty, or whitespace).
    Enhanced: Also treats empty lists, tuples, and dicts as invalid.
    """
    if value is None:
        return False
    if value == ["nan"]:
        return False
    if pd.isna(value):
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict)) and len(value) == 0:
        return False
    if isinstance(value, (int, float)):
        return not (math.isinf(value) or math.isnan(value))
    return True

def is_positive_value(value):
    """
    Check if a value is positive.
    If value is a string, try to convert to int or float.
    """
    # Try to convert string to number
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return False
        try:
            # Try integer first, then float
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
        except ValueError:
            return False
    # Now check positivity
    if isinstance(value, (int, float)) and not (math.isinf(value) or math.isnan(value)):
        return value > 0
    return False

def load_yaml_rules(yaml_path):
    with open(yaml_path, 'r') as f:
        rules = yaml.safe_load(f)
    return rules

def get_always_mandatory_columns(rules):
    return rules.get('always_mandatory', [])

def get_conditional_mandatory_columns(rules, row):
    conditional_columns = []
    for condition in rules.get('conditional_mandatory', []):
        cond = condition['condition']
        col = cond['column']
        val = cond['value']
        if row.get(col) == val:
            conditional_columns.extend(condition['required_columns'])
    return conditional_columns

def split_data_by_mandatory_columns(df, yaml_path):
    rules = load_yaml_rules(yaml_path)
    always_mandatory = get_always_mandatory_columns(rules)
    positive_columns = ['age', 'amount']

    missing_rows = []
    complete_rows = []

    for idx, row in df.iterrows():
        missing = False
        # Check always mandatory columns for validity
        for col in always_mandatory:
            if not is_valid_value(row.get(col)):
                missing = True
                break
        # Check positivity for specific columns if present
        if not missing:
            for pos_col in positive_columns:
                if pos_col in always_mandatory:
                    if not is_positive_value(row.get(pos_col)):
                        missing = True
                        break
        # Check conditional mandatory columns
        if not missing:
            cond_cols = get_conditional_mandatory_columns(rules, row)
            for col in cond_cols:
                if not is_valid_value(row.get(col)):
                    missing = True
                    break

        if missing:
            missing_rows.append(idx)
        else:
            complete_rows.append(idx)

    missing_data = df.loc[missing_rows].copy()
    complete_data = df.loc[complete_rows].copy()
    return missing_data, complete_data
