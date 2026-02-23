# Contributing to CPU-Only LLM Data Automation Pipeline

Thanks for your interest in contributing! Here are some guidelines to help you get started.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/REPO_NAME.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit with clear messages: `git commit -m "Add feature: description"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

1. Install dependencies:
   ```bash
   cd data_pipeline
   pip install -r requirements.txt
   ```

2. Install Ollama and pull a model:
   ```bash
   ollama pull mistral
   ```

3. Run tests:
   ```bash
   python test_pipeline.py
   ```

## Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and modular

## Pull Request Guidelines

- Describe what your PR does and why
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed
- Keep PRs focused on a single feature or fix

## Reporting Issues

- Use the GitHub issue tracker
- Provide clear reproduction steps
- Include your environment details (OS, Python version, Ollama version)
- Share relevant error messages or logs

## Questions?

Feel free to open an issue for questions or discussions.
