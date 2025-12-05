import jsonschema
from jsonschema import validate

# Define a schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
    },
    "required": ["name", "age"],
}

# Define JSON data
data = {
    "namey": "John Doe",
    "age": 30,
}

# Validate data
try:
    validate(instance=data, schema=schema)
    print("JSON data is valid.")
except jsonschema.exceptions.ValidationError as e:
    print(f"JSON data is invalid:")
    