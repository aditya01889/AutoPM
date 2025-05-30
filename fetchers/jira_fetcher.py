import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from jira import JIRA
from jira.exceptions import JIRAError

from .base_fetcher import BaseFetcher, Update
from config.settings import settings

logger = logging.getLogger(__name__)

class JiraFetcher(BaseFetcher):
    """Fetches updates from Jira issues"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__(config or {})
        self.jira = self._initialize_jira_client()
        self.projects = self.config.get("projects", [])
        self.lookback_days = self.config.get("lookback_days", 7)  # Default to 7 days for Jira
    
    def _initialize_jira_client(self) -> JIRA:
        """Initialize and return Jira client"""
        if not all([settings.JIRA_SERVER, settings.JIRA_EMAIL, settings.JIRA_API_TOKEN]):
            raise ValueError("Missing required Jira configuration")
            
        return JIRA(
            server=settings.JIRA_SERVER,
            basic_auth=(settings.JIRA_EMAIL, settings.JIRA_API_TOKEN)
        )
    
    async def fetch_updates(self, since: datetime = None) -> List[Update]:
        """
        Fetch updated Jira issues
        
        Args:
            since: Only fetch issues updated after this datetime
            
        Returns:
            List of Update objects
        """
        if not since:
            since = datetime.utcnow() - timedelta(days=self.lookback_days)
            
        updates = []
        
        # Build JQL query
        jql_parts = [
            "updated >= '" + since.strftime('%Y-%m-%d %H:%M') + "'"
        ]
        
        if self.projects:
            projects_str = ", ".join(f'"{p}"' for p in self.projects)
            jql_parts.append(f"project in ({projects_str})")
        
        jql = " AND ".join(jql_parts)
        
        try:
            # Fetch issues updated since the given time
            issues = self.jira.search_issues(
                jql,
                maxResults=50,  # Adjust based on needs
                fields="summary,description,status,assignee,updated,comment"
            )
            
            for issue in issues:
                # Get issue details
                issue_url = f"{self.jira.client_info()}/browse/{issue.key}"
                assignee = getattr(issue.fields.assignee, 'displayName', 'Unassigned')
                status = getattr(issue.fields.status, 'name', 'Unknown')
                
                # Get comments
                comments = []
                if hasattr(issue.fields, 'comment') and hasattr(issue.fields.comment, 'comments'):
                    comments = [
                        f"{comment.author.displayName} commented: {comment.body}"
                        for comment in issue.fields.comment.comments
                        if comment.updated and datetime.strptime(comment.updated, '%Y-%m-%dT%H:%M:%S.%f%z') >= since
                    ]
                
                # Create update for the issue
                update = Update(
                    source=f"jira:{issue.key}",
                    content=f"{issue.key}: {issue.fields.summary}\nStatus: {status}\n{'; '.join(comments)}",
                    author=getattr(issue.fields.reporter, 'displayName', 'Unknown'),
                    timestamp=datetime.strptime(issue.fields.updated, '%Y-%m-%dT%H:%M:%S.%f%z'),
                    url=issue_url,
                    metadata={
                        "key": issue.key,
                        "status": status,
                        "assignee": assignee,
                        "priority": getattr(issue.fields, 'priority', 'Unspecified'),
                        "issue_type": getattr(issue.fields.issuetype, 'name', 'Unknown')
                    }
                )
                updates.append(update)
                
        except JIRAError as e:
            logger.error(f"Error fetching Jira updates: {e}")
            
        return updates
