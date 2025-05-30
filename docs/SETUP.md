# AutoPM Setup Guide

This guide will help you set up AutoPM in your development environment.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- (Optional) Docker and Docker Compose

## Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/aditya01889/AutoPM.git
   cd AutoPM
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Run a one-time command**
   ```bash
   docker-compose run --rm app python main.py --demo
   ```

## Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

## Development Workflow

1. Make your changes
2. Run tests: `pytest`
3. Format code: `black .`
4. Lint code: `flake8`
5. Commit your changes

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

2. **Environment Variables Not Loading**
   - Make sure `.env` file exists and is properly formatted
   - Restart your terminal/IDE after creating/modifying `.env`

3. **Docker Build Fails**
   - Check Docker is running
   - Ensure you have sufficient disk space
   - Try rebuilding with `--no-cache` flag

### Getting Help

If you encounter any issues, please [open an issue](https://github.com/aditya01889/AutoPM/issues) with details about your environment and the problem you're experiencing.
