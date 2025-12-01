"""
sanitize.py

Sanitization utilities for the project.

This module provides a single helper function `sanitize_data` that ensures
input content is safe from HTML/JS injection by using bleach to clean text.
Behavior:
- If given a str, the string is sanitized with bleach.clean and returned.
- For non-str values (dict, list, numbers, etc.) the value is serialized to a
  JSON string (using json.dumps with ensure_ascii=False) and that JSON string
  is sanitized and returned.
- If serialization fails, the object's str() representation is sanitized.

Logging:
- Uses `src.logger.logger` for structured logging. The module logs whether
  serialization succeeded or fell back to string conversion.

Dependencies:
- bleach
- json (stdlib)
- src.logger (project logger module)

Example:
    from src.security.sanitize import sanitize_data
    data = {"name": "<script>bad()</script>", "age": 30}
    safe_text = sanitize_data(data)
    # safe_text is a sanitized JSON string representation of `data`

Notes:
- This function returns sanitized text (str). If you need a boolean safety
  check or a sanitized object structure, implement an alternative function.
"""
from typing import Any
import bleach
from backend.src.logger import logger

def sanitize_data(input_data: Any) -> Any:
    """
    Serialize and sanitize input data, returning a cleaned version.

    Parameters
    - input_data (Any): The data to sanitize. Can be str, dict, list, number, etc.

    Returns
    - Any: A sanitized version of the input data. Strings are cleaned, and
      other types are returned in their original form.
    """
    try:
        if isinstance(input_data, str):
            # Sanitize the string input directly
            logger.security("String data sanitized successfully", level="info")
            sanitized_input = bleach.clean(input_data)
            sanitized_input = sanitized_input.replace("'", "''")
            # Escape single quotes for SQL safety
            return sanitized_input

        elif isinstance(input_data, dict):
            # Sanitize each value in the dictionary
            logger.security("Dictionary data sanitized successfully", level="info")
            sanitized_dict = {key: sanitize_data(value) for key, value in input_data.items()}
            return sanitized_dict  # Return the sanitized dictionary without converting to JSON

        elif isinstance(input_data, list):
            # Sanitize each item in the list
            logger.security("List data sanitized successfully", level="info")
            sanitized_list = [sanitize_data(item) for item in input_data]
            return sanitized_list  # Return the sanitized list without converting to JSON

        # For numbers and booleans, return them as is
        logger.security("Non-string, non-collection data returned as is", level="info")
        return input_data
    except Exception as e:
        logger.security(f"Data sanitization failed: {e}", level="error")
        return str(input_data).replace("'", "''")  # Fallback: sanitize string representation

# Example usage
# schema = {
#     "name": "'<script>hello</script>'",
#     "age": 30,
#     "isStudent": False,
#     "skills": ["JavaScript", "Python", "HTML"],
#     "address": {
#         "street": "123 Main St",
#         "city": "Anytown",
#         "state": "CA",
#         "zip": "12345"
#     }
# }

# print("unsanitized: ", schema)

# sanitized_schema = sanitize_data(schema)

# print("sanitized: ", sanitized_schema)
