from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class SummaryItem(BaseModel):
    """A single summarized item (progress, blocker, or next step)"""
    content: str
    source: str
    metadata: Dict[str, Any] = {}

class DigestSummary(BaseModel):
    """Complete summary of all updates"""
    timestamp: datetime
    progress: List[SummaryItem] = []
    blockers: List[SummaryItem] = []
    next_steps: List[SummaryItem] = []
    
    def to_markdown(self) -> str:
        """Convert the summary to markdown format"""
        sections = [
            "# Project Update Digest",
            f"*Generated at: {self.timestamp.strftime('%Y-%m-%d %H:%M %Z')}*\n"
        ]
        
        def add_section(title: str, items: List[SummaryItem]):
            if items:
                sections.append(f"## {title}")
                for idx, item in enumerate(items, 1):
                    source = f"\n*Source: {item.source}*" if item.source else ""
                    sections.append(f"{idx}. {item.content}{source}")
                sections.append("")  # Add empty line after section
        
        add_section("Progress", self.progress)
        add_section("Blockers", self.blockers)
        add_section("Next Steps", self.next_steps)
        
        return "\n".join(sections)

class BaseSummarizer(ABC):
    """Abstract base class for all summarizers"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
    
    @abstractmethod
    async def summarize(self, updates: List[Dict]) -> DigestSummary:
        """
        Summarize a list of updates
        
        Args:
            updates: List of update dictionaries to summarize
            
        Returns:
            DigestSummary containing the summarized information
        """
        pass
