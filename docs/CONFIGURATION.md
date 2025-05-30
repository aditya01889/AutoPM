# AutoPM Configuration Guide

This guide explains how to configure AutoPM for your needs.

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Slack Configuration
SLACK_BOT_TOKEN=your-slack-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_APP_TOKEN=your-app-token

# Jira Configuration
JIRA_SERVER=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-jira-api-token

# Notion Configuration
NOTION_API_KEY=your-notion-api-key
NOTION_DATABASE_ID=your-database-id

# OpenAI Configuration (for AI summarization)
OPENAI_API_KEY=your-openai-api-key

# App Configuration
ENVIRONMENT=development  # or 'production'
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Digest Configuration
DIGEST_SCHEDULE="0 17 * * 1-5"  # Weekdays at 5 PM
TIMEZONE="America/Los_Angeles"

# Email Configuration (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com
```

## Service-Specific Setup

### Slack Setup

1. Create a new Slack App at [api.slack.com/apps](https://api.slack.com/apps)
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

1. Generate an API token at [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Use your email and the API token in the `.env` file

### Notion Setup

1. Create a new integration at [www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Share your database with the integration
3. Add the API key to your `.env` file

## Configuration Examples

### Basic Configuration

```env
ENVIRONMENT=development
LOG_LEVEL=INFO
DIGEST_SCHEDULE="0 9 * * 1-5"  # Weekdays at 9 AM
TIMEZONE="America/New_York"
```

### Email Notifications

```env
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com
```

## Customizing the Digest

You can customize the digest format by modifying the templates in the `templates/` directory.

## Logging

Logs are written to `autopm.log` by default. You can adjust the log level in the `.env` file.

## Security Considerations

- Never commit your `.env` file to version control
- Use environment-specific configuration files for different environments
- Rotate API keys and tokens regularly
- Use the principle of least privilege when setting up API permissions
