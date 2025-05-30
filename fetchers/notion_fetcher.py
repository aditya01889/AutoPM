import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from notion_client import Client

from .base_fetcher import BaseFetcher, Update
from config.settings import settings

logger = logging.getLogger(__name__)

class NotionFetcher(BaseFetcher):
    """Fetches updates from Notion databases"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__(config or {})
        self.client = self._initialize_notion_client()
        self.database_id = settings.NOTION_DATABASE_ID
        self.lookback_days = self.config.get("lookback_days", 3)
    
    def _initialize_notion_client(self) -> Client:
        """Initialize and return Notion client"""
        if not settings.NOTION_API_KEY:
            raise ValueError("Missing required Notion API key")
            
        return Client(auth=settings.NOTION_API_KEY)
    
    async def fetch_updates(self, since: datetime = None) -> List[Update]:
        """
        Fetch updated Notion pages from the configured database
        
        Args:
            since: Only fetch pages updated after this datetime
            
        Returns:
            List of Update objects
        """
        if not since:
            since = datetime.utcnow() - timedelta(days=self.lookback_days)
            
        updates = []
        
        try:
            # Query the database for recently updated pages
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "timestamp": "last_edited_time",
                    "last_edited_time": {
                        "after": since.isoformat()
                    }
                },
                sorts=[{
                    "property": "last_edited_time",
                    "direction": "descending"
                }]
            )
            
            for page in response.get("results", []):
                # Get page properties
                page_id = page["id"]
                page_url = page["url"]
                last_edited = page["last_edited_time"]
                
                # Get page title (handles different title property types)
                title = "Untitled"
                for prop_name, prop_value in page.get("properties", {}).items():
                    if prop_value.get("type") == "title" and prop_value.get("title"):
                        title = " ".join([t.get("plain_text", "") for t in prop_value["title"]])
                        break
                
                # Get page content
                content_blocks = []
                try:
                    block_children = self.client.blocks.children.list(block_id=page_id)
                    for block in block_children.get("results", []):
                        block_type = block.get("type")
                        block_content = block.get(block_type, {})
                        
                        # Extract text content from the block
                        if "rich_text" in block_content and block_content["rich_text"]:
                            text = " ".join([rt.get("plain_text", "") for rt in block_content["rich_text"]])
                            if text.strip():
                                content_blocks.append(f"{block_type.upper()}: {text}")
                except Exception as e:
                    logger.warning(f"Could not fetch content for page {page_id}: {e}")
                
                # Create update
                update = Update(
                    source=f"notion:{page_id}",
                    content=f"{title}\n\n" + "\n".join(content_blocks[:5]),  # First 5 blocks as preview
                    author=page.get("created_by", {}).get("id", "unknown"),
                    timestamp=datetime.fromisoformat(last_edited.rstrip('Z')),  # Remove 'Z' for timezone handling
                    url=page_url,
                    metadata={
                        "page_id": page_id,
                        "created_time": page.get("created_time", ""),
                        "last_edited_time": last_edited,
                        "properties": list(page.get("properties", {}).keys())
                    }
                )
                updates.append(update)
                
        except Exception as e:
            logger.error(f"Error fetching Notion updates: {e}")
            
        return updates
