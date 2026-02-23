import json
import jsonschema
from jsonschema import validate, ValidationError
from schema import SCHEMA_DEFINITION

def validate_json(data):
    """
    Validates a dictionary against the defined schema.
    Returns: (is_valid: bool, error_message: str or None)
    """
    try:
        validate(instance=data, schema=SCHEMA_DEFINITION)
        return True, None
    except ValidationError as e:
        # Create a concise error message
        return False, f"Field '{e.json_path}' - {e.message}"
    except Exception as e:
        return False, str(e)

def validate_fields_custom(data):
    """
    Add any extra Python-side logic that JSON Schema can't handle easily.
    Example: Checking if signup_date is in the past (logic not implemented here for simplicity)
    """
    return True, None
