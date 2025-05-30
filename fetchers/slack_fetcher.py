import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .base_fetcher import BaseFetcher, Update
from config.settings import settings

logger = logging.getLogger(__name__)

class SlackFetcher(BaseFetcher):
    """Fetches updates from Slack channels and threads"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__(config or {})
        self.client = WebClient(token=settings.SLACK_BOT_TOKEN)
        self.channels = self.config.get("channels", [])
        self.lookback_days = self.config.get("lookback_days", 1)
    
    async def fetch_updates(self, since: datetime = None) -> List[Update]:
        """
        Fetch messages from configured Slack channels
        
        Args:
            since: Only fetch messages after this datetime
            
        Returns:
            List of Update objects
        """
        if not since:
            since = datetime.utcnow() - timedelta(days=self.lookback_days)
        
        updates = []
        
        for channel_id in self.channels:
            try:
                # Fetch channel history
                response = self.client.conversations_history(
                    channel=channel_id,
                    oldest=since.timestamp(),
                    limit=100  # Adjust based on needs
                )
                
                for message in response.get("messages", []):
                    # Skip bot messages and thread replies (we'll handle threads separately)
                    if message.get("subtype") == "bot_message" or "thread_ts" in message:
                        continue
                        
                    # Create update for the message
                    update = Update(
                        source=f"slack:{channel_id}",
                        content=message.get("text", ""),
                        author=message.get("user", "unknown"),
                        timestamp=datetime.fromtimestamp(float(message.get("ts", 0))),
                        url=self._get_message_link(channel_id, message.get("ts")),
                        metadata={
                            "channel": channel_id,
                            "thread_ts": message.get("thread_ts"),
                            "reactions": message.get("reactions", [])
                        }
                    )
                    updates.append(update)
                    
                    # If this message has a thread, fetch thread replies
                    if "thread_ts" in message:
                        thread_updates = await self._fetch_thread_replies(channel_id, message["thread_ts"], since)
                        updates.extend(thread_updates)
                        
            except SlackApiError as e:
                logger.error(f"Error fetching Slack updates from channel {channel_id}: {e}")
        
        return updates
    
    async def _fetch_thread_replies(self, channel_id: str, thread_ts: str, since: datetime) -> List[Update]:
        """Fetch replies to a thread"""
        updates = []
        try:
            response = self.client.conversations_replies(
                channel=channel_id,
                ts=thread_ts
            )
            
            for message in response.get("messages", [])[1:]:  # Skip the first message (already processed)
                if float(message.get("ts", 0)) > since.timestamp():
                    update = Update(
                        source=f"slack:{channel_id}:thread",
                        content=message.get("text", ""),
                        author=message.get("user", "unknown"),
                        timestamp=datetime.fromtimestamp(float(message.get("ts", 0))),
                        url=self._get_message_link(channel_id, message.get("ts")),
                        metadata={
                            "channel": channel_id,
                            "thread_ts": thread_ts,
                            "is_thread_reply": True
                        }
                    )
                    updates.append(update)
                    
        except SlackApiError as e:
            logger.error(f"Error fetching thread replies for {channel_id}/{thread_ts}: {e}")
            
        return updates
    
    def _get_message_link(self, channel_id: str, ts: str) -> str:
        """Generate a direct link to a Slack message"""
        return f"https://slack.com/app_redirect?channel={channel_id}&message={ts}"
