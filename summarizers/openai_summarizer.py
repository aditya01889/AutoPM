import logging
from typing import List, Dict, Any
import json
from openai import OpenAI

from .base_summarizer import BaseSummarizer, DigestSummary, SummaryItem
from config.settings import settings

logger = logging.getLogger(__name__)

class OpenAISummarizer(BaseSummarizer):
    """Summarizes updates using OpenAI's API"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config or {})
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = self.config.get("model", "gpt-4-turbo-preview")
        self.max_tokens = self.config.get("max_tokens", 4000)
    
    async def summarize(self, updates: List[Dict]) -> DigestSummary:
        """
        Summarize updates using OpenAI's API
        
        Args:
            updates: List of update dictionaries to summarize
            
        Returns:
            DigestSummary containing the summarized information
        """
        if not updates:
            return DigestSummary(timestamp=datetime.utcnow())
        
        # Prepare the prompt with the updates
        prompt = self._build_prompt(updates)
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes project updates."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            result = json.loads(response.choices[0].message.content)
            
            # Convert to DigestSummary
            return DigestSummary(
                timestamp=datetime.utcnow(),
                progress=[
                    SummaryItem(content=item["content"], source=item.get("source", ""), metadata=item.get("metadata", {}))
                    for item in result.get("progress", [])
                ],
                blockers=[
                    SummaryItem(content=item["content"], source=item.get("source", ""), metadata=item.get("metadata", {}))
                    for item in result.get("blockers", [])
                ],
                next_steps=[
                    SummaryItem(content=item["content"], source=item.get("source", ""), metadata=item.get("metadata", {}))
                    for item in result.get("next_steps", [])
                ]
            )
            
        except Exception as e:
            logger.error(f"Error summarizing with OpenAI: {e}")
            # Fallback to a simple summary if there's an error
            return self._fallback_summary(updates)
    
    def _build_prompt(self, updates: List[Dict]) -> str:
        """Build the prompt for the OpenAI API"""
        updates_text = ""
        for i, update in enumerate(updates, 1):
            updates_text += f"""
            --- Update {i} ---
            Source: {update.get('source', 'Unknown')}
            Timestamp: {update.get('timestamp', 'Unknown')}
            Content: {update.get('content', '')}
            """
        
        return f"""
        I need you to analyze the following project updates and extract key information.
        For each update, identify:
        1. Progress made (what was accomplished)
        2. Blockers or issues encountered
        3. Next steps or action items
        
        Format your response as a JSON object with the following structure:
        {{
            "progress": [
                {{"content": "Brief description of progress", "source": "Source of the update"}},
                ...
            ],
            "blockers": [
                {{"content": "Description of blocker", "source": "Source of the update"}},
                ...
            ],
            "next_steps": [
                {{"content": "Description of next step", "source": "Source of the update"}},
                ...
            ]
        }}
        
        Updates to analyze:
        {updates_text}
        
        Be concise but informative. Group similar items together. Include the source for each item.
        """
    
    def _fallback_summary(self, updates: List[Dict]) -> DigestSummary:
        """Generate a simple summary without using the API"""
        summary = DigestSummary(timestamp=datetime.utcnow())
        
        for update in updates:
            source = update.get("source", "Unknown")
            content = update.get("content", "")
            
            # Simple heuristic: if content mentions "block" or "issue", it's a blocker
            if any(word in content.lower() for word in ["block", "issue", "problem", "can't", "cannot"]):
                summary.blockers.append(SummaryItem(content=content, source=source))
            # If content mentions "next" or "todo", it's a next step
            elif any(word in content.lower() for word in ["next", "todo", "need to", "should"]):
                summary.next_steps.append(SummaryItem(content=content, source=source))
            # Otherwise, it's progress
            else:
                summary.progress.append(SummaryItem(content=content, source=source))
        
        return summary
