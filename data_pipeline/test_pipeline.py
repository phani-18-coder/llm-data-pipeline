import sys
import os
import json
import logging

# Ensure we can import the modules
sys.path.append(os.getcwd())

try:
    from schema import get_schema_string
    from validator import validate_json
    from llm import call_ollama, parse_llm_json
    from reconciler import reconcile_data
except ImportError as e:
    print(f"FAIL: Import Error - {e}")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    logger.info("Testing Imports... OK")

def test_schema_load():
    s = get_schema_string()
    if "full_name" in s:
        logger.info("Testing Schema Load... OK")
    else:
        logger.error("FAIL: Schema load failed or content unexpected")

def test_validator():
    valid_data = {
        "full_name": "Test User",
        "email": "test@example.com",
        "age": 25,
        "account_type": "free",
        "signup_date": "2023-01-01",
        "is_active": True
    }
    is_valid, msg = validate_json(valid_data)
    if is_valid:
        logger.info("Testing Validator (Good Data)... OK")
    else:
        logger.error(f"FAIL: Validator rejected good data: {msg}")

    invalid_data = valid_data.copy()
    invalid_data["age"] = 10 # Too young
    is_valid, msg = validate_json(invalid_data)
    if not is_valid:
        logger.info("Testing Validator (Bad Data)... OK")
    else:
        logger.error(f"FAIL: Validator accepted bad data")

def test_ollama_connection():
    logger.info("Testing Ollama Connection...")
    resp = call_ollama("Say 'hello'", model="mistral") 
    # Note: If mistral isn't there, this might fail. We will see.
    if "Error" in resp:
        logger.warning(f"Ollama Connection Warning: {resp}")
        logger.warning("Make sure Ollama is running and 'mistral' is pulled.")
    else:
        logger.info(f"Ollama Response: {resp[:50]}... OK")

if __name__ == "__main__":
    print("--- Starting Diagnostics ---")
    test_imports()
    test_schema_load()
    test_validator()
    test_ollama_connection()
    print("--- Diagnostics Complete ---")
