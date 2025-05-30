# AutoPM API Reference

This document provides detailed information about AutoPM's API and extension points.

## Core Components

### 1. Fetchers

Fetchers are responsible for collecting data from various sources.

#### BaseFetcher (Abstract Class)

```python
class BaseFetcher(ABC):
    @abstractmethod
    async def fetch_updates(self) -> List[Dict]:
        """Fetch updates from the data source."""
        pass
```

#### Available Fetchers

- `SlackFetcher`: Fetches messages and updates from Slack
- `JiraFetcher`: Retrieves issues and updates from Jira
- `NotionFetcher`: Gets updates from Notion databases

### 2. Notifiers

Notifiers handle sending updates to various destinations.

#### BaseNotifier (Abstract Class)

```python
class BaseNotifier(ABC):
    @abstractmethod
    async def send(self, message: str, **kwargs) -> bool:
        """Send a notification."""
        pass
```

#### Available Notifiers

- `SlackNotifier`: Sends messages to Slack channels
- `EmailNotifier`: Sends emails with updates

### 3. Summarizers

Summarizers process and condense the collected information.

#### BaseSummarizer (Abstract Class)

```python
class BaseSummarizer(ABC):
    @abstractmethod
    async def summarize(self, updates: List[Dict]) -> str:
        """Generate a summary from the updates."""
        pass
```

#### Available Summarizers

- `OpenAISummarizer`: Uses OpenAI's API to generate AI-powered summaries

## Extending AutoPM

### Adding a New Fetcher

1. Create a new file in the `fetchers` directory
2. Implement the `BaseFetcher` interface
3. Add configuration in `config/settings.py`
4. Update the fetcher factory in `main.py`

Example:

```python
# fetchers/custom_fetcher.py
from .base_fetcher import BaseFetcher

class CustomFetcher(BaseFetcher):
    def __init__(self, config):
        self.config = config
    
    async def fetch_updates(self) -> List[Dict]:
        # Implementation here
        return []
```

### Adding a New Notifier

1. Create a new file in the `notifiers` directory
2. Implement the `BaseNotifier` interface
3. Add configuration in `config/settings.py`

### Adding a New Summarizer

1. Create a new file in the `summarizers` directory
2. Implement the `BaseSummarizer` interface
3. Update the summarizer factory in `main.py`

## API Endpoints

### Webhook Endpoints

- `POST /webhook/slack`: Handle incoming Slack webhooks
- `POST /webhook/jira`: Handle Jira webhook events
- `POST /webhook/notion`: Handle Notion webhook events

### API Endpoints

- `GET /api/status`: Get service status
- `POST /api/digest`: Trigger a manual digest
- `GET /api/health`: Health check endpoint

## Error Handling

All API endpoints return JSON responses with appropriate HTTP status codes.

### Error Response Format

```json
{
    "status": "error",
    "message": "Error description",
    "code": "ERROR_CODE",
    "details": {
        "field": "Additional error details"
    }
}
```

## Rate Limiting

API endpoints are rate limited to prevent abuse. The default rate limit is 100 requests per minute per IP address.

## Authentication

Endpoints require authentication using API keys or OAuth2 tokens, depending on the configuration.

## Webhook Security

All webhook endpoints verify the request signature to ensure they come from the expected source.
