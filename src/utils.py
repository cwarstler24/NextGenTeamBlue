from datetime import date, datetime

def convert_bytes_to_strings(obj):
    if isinstance(obj, bytes):
        return obj.decode('utf-8')
    elif isinstance(obj, (date, datetime)):
        return obj.isoformat()
    elif isinstance(obj, list):
        return [convert_bytes_to_strings(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_bytes_to_strings(value) for key, value in obj.items()}
    return obj
