# AutoPM - Autonomous Project Management Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Demo](https://img.shields.io/badge/Demo-Available-green)](https://github.com/aditya01889/AutoPM#-quick-start)

> **Note**: Try the demo with sample data - no API keys required!

AutoPM is an AI-powered assistant for Technical Program Managers (TPMs) that automates the process of gathering project updates, summarizing key information, and distributing digests to the team.

## 🌟 Features

- **Multi-source Integration**: Pull updates from Slack, Jira, and Notion
- **AI-Powered Summarization**: Generate concise summaries using AI
- **Automated Scheduling**: Configure daily/weekly digests
- **Multiple Output Channels**: Deliver updates via Slack or Email
- **Extensible Architecture**: Easily add new data sources and outputs

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker (optional)

### Running the Demo

```bash
# Clone the repository
git clone https://github.com/aditya01889/AutoPM.git
cd AutoPM

# Option 1: Run with Docker (recommended)
docker-compose up --build

# Option 2: Run locally
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
python run_demo.py
```

## 🖼️ Demo Output

```
🚀 Starting AutoPM Demo
----------------------------------------
📋 Sample Updates from Different Sources:

🔹 SLACK:
   • Team meeting scheduled for tomorrow at 10 AM
   • New feature request from @alice: Add dark mode support
   • Bug reported by @bob: Login page not loading on mobile

🔹 JIRA:
   • [PROJ-123] Implement user authentication - In Progress
   • [PROJ-124] Fix login page layout - Done
   • [PROJ-125] Add password reset feature - To Do

🔹 NOTION:
   • Project timeline updated: Phase 1 completion delayed by 2 days
   • New document added: API Documentation v1.2
   • Meeting notes from 2023-05-30 uploaded

🤖 Generating AI Summary...

📊 Project Status Summary (Demo)
----------------------------
• Authentication module is 80% complete
• Mobile responsiveness issues need attention
• Team is on track for the sprint goal
• 3 high-priority tasks to address

✅ Demo completed successfully!
```

## 🏗️ Project Structure

```
AutoPM/
├── config/           # Configuration files
├── docs/             # Documentation
├── fetchers/         # Data source integrations
├── notifiers/        # Output channels
├── summarizers/      # AI summarization logic
├── tests/            # Test suite
├── .env.example      # Example environment variables
├── main.py           # Main application entry point
├── run_demo.py       # Demo script
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## 📚 Documentation

For detailed documentation, please see the [docs](docs/) directory.

- [Setup Guide](docs/SETUP.md)
- [Configuration](docs/CONFIGURATION.md)
- [API Reference](docs/API.md)
- [Screenshots](docs/SCREENSHOTS.md)

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python
- Uses various third-party APIs (Slack, Jira, Notion)
- Inspired by modern project management workflows

## Prerequisites

- Python 3.8+
- API keys for the services you want to use (Slack, Jira, Notion, OpenAI)
- SMTP credentials if using email notifications

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/autopm.git
   cd autopm
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the example environment file and update it with your API keys:
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file with your actual API keys and configuration.

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_APP_TOKEN=xapp-your-app-token

# Jira Configuration
JIRA_SERVER=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-jira-api-token

# Notion Configuration
NOTION_API_KEY=your-notion-api-key
NOTION_DATABASE_ID=your-database-id

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# App Configuration
ENVIRONMENT=development
LOG_LEVEL=INFO

# Digest Configuration
DIGEST_SCHEDULE="0 17 * * 1-5"  # Weekdays at 5 PM
TIMEZONE="America/Los_Angeles"

# Email Configuration (if using email notifier)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com
```

### Slack App Setup

1. Create a new Slack App at https://api.slack.com/apps
2. Add the following OAuth scopes:
   - `channels:history`
   - `channels:read`
   - `chat:write`
   - `groups:history`
   - `im:history`
   - `mpim:history`
   - `users:read`
3. Install the app to your workspace
4. Add the bot token to your `.env` file

### Jira Setup

1. Generate an API token at https://id.atlassian.com/manage-profile/security/api-tokens
2. Use your email and the API token in the `.env` file

### Notion Setup

1. Create a new integration at https://www.notion.so/my-integrations
2. Share your database with the integration
3. Use the integration token in the `.env` file

## Usage

### Running AutoPM

```bash
python main.py
```

### Running a One-Time Digest

Uncomment the following lines in `main.py` and run the script:

```python
# For testing: Run a digest cycle immediately
await autopm.run_digest_cycle()
```

### Configuration Options

You can configure the following in `main.py`:

- Data sources (Slack channels, Jira projects, Notion databases)
- Digest schedule
- Output channels (Slack channels, email recipients)
- Summarization settings

## Project Structure

```
autopm/
├── config/                  # Configuration files
│   └── settings.py          # Application settings
├── fetchers/                # Data source integrations
│   ├── base_fetcher.py      # Abstract base class for fetchers
│   ├── slack_fetcher.py     # Slack integration
│   ├── jira_fetcher.py      # Jira integration
│   └── notion_fetcher.py    # Notion integration
├── notifiers/               # Output channel integrations
│   ├── base_notifier.py     # Abstract base class for notifiers
│   ├── slack_notifier.py    # Slack notifications
│   └── email_notifier.py    # Email notifications
├── summarizers/             # Summarization logic
│   ├── base_summarizer.py   # Abstract base class for summarizers
│   └── openai_summarizer.py # OpenAI-powered summarization
├── scheduler/               # Scheduling logic
│   └── digest_scheduler.py  # Digest scheduling
├── .env.example             # Example environment variables
├── main.py                  # Main application entry point
├── README.md                # This file
└── requirements.txt         # Python dependencies
```

## Extending AutoPM

### Adding a New Data Source

1. Create a new file in the `fetchers` directory
2. Create a class that inherits from `BaseFetcher`
3. Implement the `fetch_updates` method
4. Update `main.py` to include your new fetcher

### Adding a New Output Channel

1. Create a new file in the `notifiers` directory
2. Create a class that inherits from `BaseNotifier`
3. Implement the `send` method
4. Update `main.py` to include your new notifier

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Support

For support, please open an issue in the GitHub repository.
