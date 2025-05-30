# AutoPM - Autonomous Project Management Assistant

AutoPM is an AI-powered assistant for Technical Program Managers (TPMs) that automates the process of gathering project updates, summarizing key information, and distributing digests to the team.

## Features

- **Multi-source Integration**: Pulls updates from Slack, Jira, and Notion
- **AI-Powered Summarization**: Uses OpenAI's GPT models to generate concise summaries
- **Automated Scheduling**: Sends daily/weekly digests on a configurable schedule
- **Multiple Output Channels**: Delivers digests via Slack and/or Email
- **Extensible Architecture**: Easy to add new data sources and output channels

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
