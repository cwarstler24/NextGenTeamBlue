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

import bleach
import json
from typing import Any
from src.logger import logger

def sanitize_data(input_data: Any) -> str:
    """
    Serialize and sanitize input data, returning a cleaned string.

    Parameters
    - input_data (Any): The data to sanitize. Can be str, dict, list, number, etc.

    Returns
    - str: A bleach-cleaned string. For non-string input this will be the
      JSON serialization (or str() fallback) after cleaning.

    Behavior
    - Strings: cleaned and returned.
    - Other types: json.dumps(..., ensure_ascii=False) -> cleaned -> returned.
    - On json serialization error, falls back to str(input_data), logs a warning,
      and returns the cleaned string form.

    Logging
    - On successful serialization: logger.security("Data sanitized successfully", level="info")
    - On serialization fallback: logger.security("Data serialization failed; sanitized string representation", level="warning")

    Example:
        >>> sanitize_data("<b>hi</b>")
        '&lt;b&gt;hi&lt;/b&gt;'
        >>> sanitize_data({"k": "<script/>"})
        '{"k":"&lt;script/&gt;"}'  # sanitized JSON string
    """
    if isinstance(input_data, str):
        return bleach.clean(input_data)

    try:
        # serialize to JSON (preserve unicode), then sanitize the JSON string
        json_text = json.dumps(input_data, ensure_ascii=False)
        logger.security("Data sanitized successfully", level="info")
    except (TypeError, ValueError):
        # fallback for non-serializable objects
        json_text = str(input_data)
        logger.security("Data serialization failed; sanitized string representation", level="warning")

    return bleach.clean(json_text)


# shcema = {
    
#     "name": "<script>John Doe</script>",
#     "age": 30,
#     "isStudent": False,
#     "skills": ["JavaScript", "Python", "HTML"],
#     "address": {
#     "street": "123 Main St",
#     "city": "Anytown",
#     "state": "CA",
#     "zip": "12345"
  
# }

# }

# print(shcema)

# sanitized_schema = sanitize_data(shcema)

# print(sanitized_schema)
