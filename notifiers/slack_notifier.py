import logging
from typing import Dict, Any, Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .base_notifier import BaseNotifier, NotificationResult
from config.settings import settings

logger = logging.getLogger(__name__)

class SlackNotifier(BaseNotifier):
    """Sends notifications to Slack channels"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config or {})
        self.client = WebClient(token=settings.SLACK_BOT_TOKEN)
        self.default_channel = self.config.get("default_channel", "#general")
    
    async def send(self, content: str, **kwargs) -> NotificationResult:
        """
        Send a message to a Slack channel
        
        Args:
            content: The message content (supports markdown)
            **kwargs: Additional arguments:
                - channel: The channel to send to (defaults to default_channel)
                - thread_ts: Optional timestamp of a thread to reply to
                
        Returns:
            NotificationResult indicating success or failure
        """
        channel = kwargs.get("channel", self.default_channel)
        thread_ts = kwargs.get("thread_ts")
        
        try:
            # Split long messages into chunks if needed (Slack has a limit of ~4000 chars per message)
            max_length = 3000  # Conservative limit to account for formatting
            chunks = [content[i:i+max_length] for i in range(0, len(content), max_length)]
            
            # Send the first chunk
            response = self.client.chat_postMessage(
                channel=channel,
                text=chunks[0],
                thread_ts=thread_ts,
                mrkdwn=True
            )
            
            # If there are more chunks, send them as thread replies
            thread_ts = response["ts"]
            for chunk in chunks[1:]:
                self.client.chat_postMessage(
                    channel=channel,
                    text=chunk,
                    thread_ts=thread_ts,
                    mrkdwn=True
                )
            
            return NotificationResult(
                success=True,
                message=f"Message sent to {channel}",
                details={"channel": channel, "thread_ts": thread_ts}
            )
            
        except SlackApiError as e:
            error_message = f"Error sending Slack message: {e.response['error']}"
            logger.error(error_message)
            return NotificationResult(
                success=False,
                message=error_message,
                details={"error": str(e), "channel": channel}
            )
        except Exception as e:
            error_message = f"Unexpected error sending Slack message: {str(e)}"
            logger.error(error_message, exc_info=True)
            return NotificationResult(
                success=False,
                message=error_message,
                details={"error": str(e), "channel": channel}
            )
