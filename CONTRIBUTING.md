# Contributing to AutoPM

Thank you for your interest in contributing to AutoPM! We welcome contributions from the community.

## How to Contribute

1. **Fork** the repository on GitHub
2. **Clone** the project to your own machine
3. **Commit** changes to your own branch
4. **Push** your work back up to your fork
5. Submit a **Pull Request** so we can review your changes

## Development Setup

1. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

3. Set up pre-commit hooks (optional but recommended):
   ```bash
   pre-commit install
   ```

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep lines under 88 characters (Black's default)

## Testing

Please ensure all new code is covered by tests. To run the test suite:

```bash
pytest
```

## Reporting Issues

When reporting issues, please include:

- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Any relevant error messages
- Your environment (OS, Python version, etc.)

## Feature Requests

For feature requests, please:

1. Check if the feature has already been requested
2. Clearly describe the problem you're trying to solve
3. Explain why this feature would be valuable

## Code of Conduct

This project adheres to the [Contributor Covenant](https://www.contributor-covenant.org/). By participating, you are expected to uphold this code.
