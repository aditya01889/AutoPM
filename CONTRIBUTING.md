# Contributing to AutoPM

Thank you for your interest in contributing to AutoPM! We welcome contributions from the community. By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

1. **Check Existing Issues**: Before creating a new issue, please check if a similar issue already exists.
2. **Create an Issue**: If you find a bug, please create a new issue with a clear title and description.
   - Include steps to reproduce the issue
   - Add error messages or screenshots if applicable
   - Specify your environment (OS, Python version, etc.)

### Suggesting Enhancements

1. **Describe the Feature**: Clearly explain the new feature or enhancement.
2. **Explain Why**: Describe why this feature would be valuable.
3. **Provide Examples**: If possible, provide examples of the proposed changes.

### Making Code Contributions

1. **Fork the Repository**
2. **Create a Branch**: Use a descriptive branch name (e.g., `feature/add-slack-commands`)
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Your Changes**: Follow the coding standards and write tests for new features.
4. **Run Tests**: Ensure all tests pass before submitting a pull request.
   ```bash
   pytest tests/
   ```
5. **Commit Your Changes**: Write clear, concise commit messages.
   ```bash
   git commit -m "Add feature: brief description of changes"
   ```
6. **Push to Your Fork**:
   ```bash
   git push origin your-branch-name
   ```
7. **Create a Pull Request**:
   - Reference any related issues
   - Describe your changes in detail
   - Request review from maintainers

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
