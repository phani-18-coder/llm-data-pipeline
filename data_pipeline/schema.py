import json

# Define the target structure validation schema using standard JSON Schema
# Let's assume we are processing "User Registration" data as a generic example case
# Fields: full_name (string), email (email format), age (int, 18-120), account_type (enum), is_active (bool)

SCHEMA_DEFINITION = {
    "type": "object",
    "properties": {
        "full_name": {
            "type": "string",
            "minLength": 2,
            "description": "Full legal name of the user"
        },
        "email": {
            "type": "string",
            "format": "email",
             "pattern": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$",
            "description": "Valid email address"
        },
        "age": {
            "type": "integer",
            "minimum": 18,
            "maximum": 120,
            "description": "User age in years"
        },
        "account_type": {
            "type": "string",
            "enum": ["free", "pro", "enterprise"],
            "description": "Subscription tier"
        },
        "signup_date": {
            "type": "string",
            "format": "date",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
            "description": "ISO 8601 date string (YYYY-MM-DD)"
        },
        "is_active": {
            "type": "boolean",
            "description": "Whether the account is currently active"
        }
    },
    "required": ["full_name", "email", "age", "account_type", "signup_date", "is_active"],
    "additionalProperties": False
}

def get_schema_string():
    """Returns the schema as a formatted string for the LLM prompt"""
    return json.dumps(SCHEMA_DEFINITION, indent=2)
