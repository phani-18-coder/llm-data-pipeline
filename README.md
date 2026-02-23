# 🤖 CPU-Only LLM Data Automation Pipeline

Convert messy CSV/Excel data into validated JSON using local LLM (Ollama). A fully automated data pipeline with validation, auto-correction, and reconciliation - all running on your CPU without cloud APIs.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Ollama](https://img.shields.io/badge/ollama-compatible-orange.svg)

## ✨ Features

- **Local LLM Processing**: Uses Ollama for privacy-focused, offline data transformation
- **Smart Validation**: Automatic JSON schema validation with retry logic
- **Auto-Correction**: Self-healing pipeline that fixes errors automatically
- **Reconciliation**: Detects hallucinations by comparing input vs output
- **Interactive UI**: Built with Streamlit for easy data processing
- **Mock Mode**: Test the pipeline without Ollama installed
- **CPU-Only**: No GPU required - runs on any machine

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+**
2. **Ollama** - [Download here](https://ollama.com/)
3. **Pull a model**:
   ```bash
   ollama pull mistral
   ```

### Installation

```bash
# Clone the repository
git clone https://github.com/phani-18-coder/llm-data-pipeline.git
cd llm-data-pipeline

# Install dependencies
cd data_pipeline
pip install -r requirements.txt
```

### Usage

1. **Start Ollama** (in one terminal):
   ```bash
   ollama serve
   ```

2. **Run the app** (in another terminal):
   ```bash
   cd data_pipeline
   streamlit run app.py
   ```

3. **Process your data**:
   - Upload `data/sample.csv` or your own CSV/Excel file
   - Click "Start Processing"
   - Watch the AI validate and correct your data in real-time

## 📁 Project Structure

```
llm-data-pipeline/
├── data_pipeline/
│   ├── app.py              # Main Streamlit application
│   ├── llm.py              # Ollama API integration
│   ├── schema.py           # JSON schema definitions
│   ├── validator.py        # Schema validation logic
│   ├── reconciler.py       # Hallucination detection
│   ├── test_pipeline.py    # Unit tests
│   ├── datagen.py          # Sample data generator
│   ├── requirements.txt    # Python dependencies
│   └── data/
│       ├── sample.csv      # Test data with errors
│       └── large_sample.csv
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

## 🎯 How It Works

1. **Upload Data**: CSV or Excel files with messy, unstructured data
2. **LLM Processing**: Each row is sent to Ollama for structured extraction
3. **Validation**: Output is validated against a JSON schema
4. **Auto-Fix**: Failed validations trigger automatic correction attempts
5. **Reconciliation**: Checks for data hallucinations or missing fields
6. **Export**: Download valid JSON or review errors for manual fixes

## 🛠️ Customization

### Change the Schema

Edit `data_pipeline/schema.py` to match your data structure:

```python
SCHEMA_DEFINITION = {
    "type": "object",
    "properties": {
        "your_field": {"type": "string"},
        # Add your fields here
    },
    "required": ["your_field"]
}
```

### Use Different Models

In the Streamlit sidebar, enter any Ollama model:
- `mistral` (default)
- `llama3`
- `gemma`
- `phi3`

## 🧪 Testing

```bash
cd data_pipeline
python test_pipeline.py
```

## 📊 Sample Data

The project includes test data with intentional errors:
- Missing fields
- Incorrect formats
- Typos and inconsistencies

Perfect for testing the auto-correction capabilities.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Ollama](https://ollama.com/) for local LLM inference
- UI powered by [Streamlit](https://streamlit.io/)
- Inspired by the need for privacy-focused data automation

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: This pipeline runs entirely on your CPU. Processing speed depends on your hardware and the chosen model size.
