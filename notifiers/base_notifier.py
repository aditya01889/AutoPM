from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class NotificationResult(BaseModel):
    """Result of a notification attempt"""
    success: bool
    message: str
    details: Dict[str, Any] = {}

class BaseNotifier(ABC):
    """Abstract base class for all notifiers"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
    
    @abstractmethod
    async def send(self, content: str, **kwargs) -> NotificationResult:
        """
        Send a notification
        
        Args:
            content: The content to send
            **kwargs: Additional arguments specific to the notifier
            
        Returns:
            NotificationResult indicating success or failure
        """
        pass
    
    def get_notifier_name(self) -> str:
        """Return a human-readable name for the notifier"""
        return self.__class__.__name__.replace("Notifier", "").lower()
