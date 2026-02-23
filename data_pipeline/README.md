# CPU-Only LLM Data Automation Pipeline

This project converts messy CSV/Excel data into validated structured JSON using a local LLM (Ollama).

## Prerequisites

1.  **Install Python 3.9+**
2.  **Install Ollama**: [Download here](https://ollama.com/)
3.  **Pull a lightweight model**:
    ```bash
    ollama pull mistral
    # OR
    ollama pull llama3
    ```
    (Make sure to update the model name in the app sidebar if you use something other than `mistral`).

## Installation

1.  Navigate to the project folder:
    ```bash
    cd data_pipeline
    ```
2.  Install Python dependencies:
    ```bash
    pip install streamlit pandas jsonschema openpyxl requests
    ```

## Usage

1.  **Start Ollama Server** (if not already running):
    ```bash
    ollama serve
    ```
    *Keep this terminal window open.*

2.  **Run the Streamlit App**:
    Open a new terminal in the `data_pipeline` folder:
    ```bash
    streamlit run app.py
    ```

3.  **Process Data**:
    - The browser will open the app.
    - Upload the provided `data/sample.csv`.
    - Click **Start Processing**.
    - Watch as the AI processes each row, validates it, and auto-corrects errors.

## Project Structure

- `app.py`: Main UI and pipeline orchestrator.
- `llm.py`: Handles communication with Ollama.
- `schema.py`: Defines the expected JSON structure.
- `validator.py`: Validates LLM output against the schema.
- `reconciler.py`: Checks for hallucinations by comparing input vs output.
- `data/sample.csv`: Test data with intentional errors.

## Customization

- **Change Schema**: Edit `schema.py` to match your own data requirements.
- **Change Model**: Type a different model name (e.g., `llama3`, `gemma`) in the Streamlit Sidebar.
