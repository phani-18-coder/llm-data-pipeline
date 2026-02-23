import streamlit as st
import pandas as pd
import json
import time
from llm import generate_json_from_row, fix_json_with_feedback, OLLAMA_URL
from schema import get_schema_string, SCHEMA_DEFINITION
from validator import validate_json
from reconciler import reconcile_data
import requests

st.set_page_config(page_title="CPU-LLM Data Pipeline", layout="wide")

def check_ollama():
    try:
        requests.get(OLLAMA_URL.replace("/api/generate", ""), timeout=1)
        return True
    except:
        return False

# --- UI Setup ---
st.title("🤖 CPU-Only LLM Data Automation Pipeline")
st.markdown("Convert messy CSV/Excel to validated JSON using local Ollama.")

# Sidebar
st.sidebar.header("Configuration")

ollama_status = check_ollama()
status_color = "green" if ollama_status else "red"
status_text = "Running" if ollama_status else "Not Detected"
st.sidebar.markdown(f"**Ollama Status:** :{status_color}[{status_text}]")

use_mock = st.sidebar.checkbox("Use Mock Mode (Demo)", value=not ollama_status, help="Simulate LLM responses for testing without Ollama.")

model_name = st.sidebar.text_input("Ollama Model Name", value="mistral", disabled=use_mock)
max_retries = st.sidebar.slider("Max Auto-Fix Retries", 0, 5, 3)

if not ollama_status and not use_mock:
    st.warning("⚠️ Ollama is not running. Please start it or enable **Mock Mode** to test the specific app logic.")

# --- Main Logic ---
uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file:
    # Read Data
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.subheader("Raw Data Preview")
        st.dataframe(df.head())
        
        if st.button("Start Processing"):
            results = []
            valid_records = []
            error_records = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_rows = len(df)
            schema_str = get_schema_string()
            
            for index, row in df.iterrows():
                # Update UI
                progress = (index + 1) / total_rows
                progress_bar.progress(progress)
                status_text.text(f"Processing Row {index + 1}/{total_rows}...")
                
                # 1. Generate Initial JSON
                row_str = row.to_string()
                json_data = generate_json_from_row(row_str, schema_str, model=model_name, mock_mode=use_mock)
                
                # Handle initial parse failure
                if "error" in json_data and "Failed to parse" in json_data["error"]:
                    # Retry once essentially or just mark as fail
                    pass 

                # 2. Validation Loop
                is_valid, validation_error = validate_json(json_data)
                attempts = 0
                
                while not is_valid and attempts < max_retries:
                    attempts += 1
                    status_text.text(f"Row {index + 1}: Check failed. Auto-fixing attempt {attempts}...")
                    json_data = fix_json_with_feedback(json_data, validation_error, schema_str, model=model_name, mock_mode=use_mock)
                    is_valid, validation_error = validate_json(json_data)
                
                # 3. Reconciliation (only if valid or partially valid)
                reconcile_warnings = []
                if not "error" in json_data:
                    reconcile_warnings = reconcile_data(row, json_data)
                
                # 4. Segment Results
                record = {
                    "original_index": index,
                    "original_data": row.to_dict(),
                    "generated_json": json_data,
                    "is_valid": is_valid,
                    "validation_error": validation_error,
                    "reconciliation_warnings": reconcile_warnings,
                    "fix_attempts": attempts
                }
                
                results.append(record)
                
                if is_valid:
                    valid_records.append(json_data)
                else:
                    error_records.append(record)

            status_text.text("Processing Complete!")
            
            # --- Display Results ---
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.success(f"✅ Valid Records: {len(valid_records)}")
                if valid_records:
                    st.json(valid_records, expanded=False)
                    st.download_button(
                        "Download Valid JSON",
                        data=json.dumps(valid_records, indent=2),
                        file_name="valid.json",
                        mime="application/json"
                    )

            with col2:
                st.error(f"❌ Records with Errors: {len(error_records)}")
                if error_records:
                    st.write("Review & Edit Failed Records:")
                    for err in error_records:
                        with st.expander(f"Row {err['original_index']} - {err['validation_error']}"):
                            st.write("**Original:**", err['original_data'])
                            st.write("**Last Generated:**")
                            st.json(err['generated_json'])
                            if err['reconciliation_warnings']:
                                st.warning(f"Reconciliation Warnings: {err['reconciliation_warnings']}")
            
            if error_records:
                st.download_button(
                    "Download Error Log",
                    data=json.dumps(error_records, indent=2),
                    file_name="errors.json",
                    mime="application/json"
                )
                
    except Exception as e:
        st.error(f"Error reading file: {e}")

