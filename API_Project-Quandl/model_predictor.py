# Assuming 'df' is your DataFrame with a column 'adjustmentReasonCode' containing lists as strings
# For example: "[item1, item2, item3]" or "['item1', 'item2']"

# Method 1: Using string manipulation and counting commas
# This is a simple approach but may not work for all cases
df['adjustmentReasonCode_count'] = df['adjustmentReasonCode'].apply(
    lambda x: 0 if x == '[]' else (x.count(',') + 1) if isinstance(x, str) else 0
)

# Method 2: Using literal_eval to parse the string into an actual list
# This is more robust but slightly more computationally expensive
import ast
def count_list_elements(value):
    try:
        if isinstance(value, str):
            # Convert string representation of list to actual list
            parsed_list = ast.literal_eval(value)
            if isinstance(parsed_list, list):
                return len(parsed_list)
        return 0  # Return 0 for non-list values or empty lists
    except:
        return 0  # Return 0 for values that can't be parsed

df['adjustmentReasonCode_count'] = df['adjustmentReasonCode'].apply(count_list_elements)

# Method 3: Using regex for more complex list formats
# This can be helpful if the list format is inconsistent
import re
def count_elements_regex(value):
    try:
        if isinstance(value, str) and value.strip().startswith('[') and value.strip().endswith(']'):
            # Remove the brackets
            content = value[1:-1].strip()
            if not content:  # Empty list
                return 0
            # Count elements by splitting on commas not within quotes
            matches = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")++', content)
            return len(matches)
        return 0
    except:
        return 0

df['adjustmentReasonCode_count'] = df['adjustmentReasonCode'].apply(count_elements_regex)
