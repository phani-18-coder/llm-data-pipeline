import requests
import json
import time
import random

# Default Ollama URL
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "mistral"

# Mock Data Generator for Fallback
def generate_mock_response(prompt):
    """
    Generates a fake but valid JSON response for demonstration purposes
    when Ollama is not available.
    """
    time.sleep(1.5) # Simulate latency
    
    # Analyze prompt to guess intent (very basic)
    lower_prompt = prompt.lower()
    
    if "john doe" in lower_prompt:
        return json.dumps({
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "age": 34,
            "account_type": "pro",
            "signup_date": "2023-01-15",
            "is_active": True
        })
    elif "jane smith" in lower_prompt:
        return json.dumps({
            "full_name": "Jane Smith",
            "email": "jane.smith@test.com", # Fixed email
            "age": 29,
            "account_type": "free",
            "signup_date": "2023-02-20",
            "is_active": True
        })
    elif "bob" in lower_prompt:
        return json.dumps({
            "full_name": "Robert Brown",
            "email": "bob.brown@company.org",
            "age": 120, # Edge case
            "account_type": "enterprise",
            "signup_date": "2022-12-12",
            "is_active": True
        })
    elif "alice" in lower_prompt:
        # Intentionally return invalid/partial to test validation
        return json.dumps({
            "full_name": "Alice Invalid",
            "email": "alice_at_invalid", 
            "age": 17,
            "account_type": "basic",
            "signup_date": "2023-05-01",
            "is_active": False
        })
    
    # Generic fallback
    return json.dumps({
        "full_name": "Mock Generated User",
        "email": "mock@example.com",
        "age": 30,
        "account_type": "free",
        "signup_date": "2024-01-01",
        "is_active": True
    })

def call_ollama(prompt, model=DEFAULT_MODEL, stream=False, mock_mode=False):
    """
    Sends a prompt to the local Ollama instance.
    If mock_mode is True or connection fails, uses mock generator.
    """
    if mock_mode:
        return generate_mock_response(prompt)

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream,
        "format": "json"
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=10)
        response.raise_for_status()
        
        if stream:
            return response.text
        
        result = response.json()
        return result.get("response", "")
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        # Auto-fallback could be dangerous, handled by caller or explicit mode
        print("Warning: Connection to Ollama failed.")
        return '{"error": "Ollama Connection Failed"}'
    except Exception as e:
        return f'{{"error": "{str(e)}"}}'

def generate_json_from_row(row_str, schema_str, model=DEFAULT_MODEL, mock_mode=False):
    """
    First pass: Convert raw CSV row string to JSON based on schema.
    """
    prompt = f"""
    You are a data transformation agent. Convert the following unstructured or semi-structured data row into a valid JSON object matching the schema.
    
    Schema:
    {schema_str}
    
    Rules:
    1. Output ONLY valid JSON.
    2. Do not include markdown formatting (like ```json).
    3. Infer types (integers, booleans) correctly.
    4. Normalize dates to YYYY-MM-DD.
    5. If a field is missing, try to infer it or use null/default if compatible, but prefer accuracy.
    
    Data Row:
    {row_str}
    """
    
    response_text = call_ollama(prompt, model=model, mock_mode=mock_mode)
    return parse_llm_json(response_text)

def fix_json_with_feedback(previous_json, error_msg, schema_str, model=DEFAULT_MODEL, mock_mode=False):
    """
    Correction loop: Fix the invalid JSON based on the validation error.
    """
    # For mock mode, if asked to fix, just return a fixed version of the generic fallback
    if mock_mode:
        time.sleep(1)
        # Naive fix for demo: just return a valid dummy
        return {
            "full_name": previous_json.get("full_name", "Fixed User"),
            "email": "fixed@example.com",
            "age": 21,
            "account_type": "free",
            "signup_date": "2023-01-01",
            "is_active": True
        }

    prompt = f"""
    The following JSON failed validation. Please fix it according to the error message and schema.
    
    Schema:
    {schema_str}
    
    Invalid JSON:
    {json.dumps(previous_json)}
    
    Error Message:
    {error_msg}
    
    Output ONLY the corrected valid JSON.
    """
    
    response_text = call_ollama(prompt, model=model)
    return parse_llm_json(response_text)

def parse_llm_json(text):
    """
    Helper to clean and parse LLM output.
    """
    if isinstance(text, dict): 
        return text # Already parsed (mock return)

    try:
        # Clean potential markdown
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw_output": text}
