import pandas as pd
import yaml
import math

def is_valid_value(value):
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
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return False
        try:
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
        except ValueError:
            return False
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

def find_missing_columns(row, always_mandatory, positive_columns, cond_cols):
    missing_cols = []
    # Always mandatory columns
    for col in always_mandatory:
        if not is_valid_value(row.get(col)):
            missing_cols.append(col)
        elif col in positive_columns and not is_positive_value(row.get(col)):
            missing_cols.append(col)
    # Conditional mandatory columns
    for col in cond_cols:
        if not is_valid_value(row.get(col)):
            missing_cols.append(col)
    return missing_cols

def split_data_by_mandatory_columns(df, yaml_path):
    rules = load_yaml_rules(yaml_path)
    always_mandatory = get_always_mandatory_columns(rules)
    positive_columns = ['age', 'amount']

    missing_rows = []
    complete_rows = []
    key_drivers_list = []

    for idx, row in df.iterrows():
        cond_cols = get_conditional_mandatory_columns(rules, row)
        missing_cols = find_missing_columns(row, always_mandatory, positive_columns, cond_cols)

        if missing_cols:
            # Format as requested: [col1 | 1.0| col2 | 1.0]
            key_drivers = ' | '.join([f"{col} | 1.0" for col in missing_cols])
            key_drivers_list.append([key_drivers])
            missing_rows.append(idx)
        else:
            key_drivers_list.append([])
            complete_rows.append(idx)

    # Assign KeyDrivers column
    df = df.copy()
    df['KeyDrivers'] = key_drivers_list

    missing_data = df.loc[missing_rows].copy()
    complete_data = df.loc[complete_rows].copy()
    return missing_data, complete_data
