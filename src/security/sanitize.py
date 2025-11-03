import bleach
import json
from typing import Any
# from src.logger import logger

def sanitize_data(input_data: Any) -> str:
    """
    Sanitize input by serializing non-string data to JSON and cleaning the resulting text.

    - If input_data is a str: return bleach.clean(input_data)
    - Otherwise: serialize with json.dumps(...) and return bleach.clean(json_text)
    """
    if isinstance(input_data, str):
        return bleach.clean(input_data)

    try:
        # serialize to JSON (preserve unicode), then sanitize the JSON string
        json_text = json.dumps(input_data, ensure_ascii=False)
        #logger.security("Data sanitized successfully", level="info")
    except (TypeError, ValueError):
        # fallback for non-serializable objects
        json_text = str(input_data)
        #logger.security("Data serialization failed; sanitized string representation", level="warning")

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
