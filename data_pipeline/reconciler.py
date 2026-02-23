def reconcile_data(original_row, generated_json):
    """
    Compares the original CSV row data with the generated JSON to detect hallucinations or data loss.
    Returns a list of reconciliation warnings.
    """
    warnings = []
    
    # Convert original row values to string for loose comparison
    original_values = [str(v).lower() for v in original_row.values()]
    original_text = " ".join(original_values)
    
    # Check if critical data from JSON exists roughly in original input
    # (This is a heuristic check, not perfect)
    for key, value in generated_json.items():
        if value is None:
            continue
            
        val_str = str(value).lower()
        
        # Skip checking boolean flags or common small words if deemed noisy
        if len(val_str) < 2:
            continue
            
        # If the generated value (e.g., a specific name or email) isn't in the source text, flag it
        # This catches "hallucinated" data, though it might flag transformed data (e.g. date formatting)
        if val_str not in original_text:
            # Heuristic exemptions
            # If it's a date, it might have been reformatted.
            if key == "signup_date":
                continue 
            
            warnings.append(f"Potential mismatch: Field '{key}' value '{value}' not found in original source.")

    return warnings
