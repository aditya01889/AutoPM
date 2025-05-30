from abc import ABC, abstractmethod
from typing import Dict, List, Any
from datetime import datetime, timedelta
from pydantic import BaseModel

class Update(BaseModel):
    """Represents an update from a source (Slack, Jira, etc.)"""
    source: str
    content: str
    author: str = ""
    timestamp: datetime
    url: str = ""
    metadata: Dict[str, Any] = {}

class BaseFetcher(ABC):
    """Abstract base class for all fetchers"""
    
    def __init__(self, config: Dict):
        self.config = config
    
    @abstractmethod
    async def fetch_updates(self, since: datetime = None) -> List[Update]:
        """
        Fetch updates from the source
        
        Args:
            since: Only fetch updates after this datetime
            
        Returns:
            List of Update objects
        """
        pass
    
    def get_source_name(self) -> str:
        """Return a human-readable name for the source"""
        return self.__class__.__name__.replace("Fetcher", "").lower()
