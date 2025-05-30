#!/usr/bin/env python3
"""
AutoPM - Autonomous Project Management Assistant

This application automates the process of gathering updates from various sources,
summarizing them, and distributing digests to the team.
"""
import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('autopm.log')
    ]
)
logger = logging.getLogger(__name__)

# Import local modules
from config.settings import settings
from fetchers.slack_fetcher import SlackFetcher
from fetchers.jira_fetcher import JiraFetcher
from fetchers.notion_fetcher import NotionFetcher
from summarizers.openai_summarizer import OpenAISummarizer
from notifiers.slack_notifier import SlackNotifier
from notifiers.email_notifier import EmailNotifier
from scheduler.digest_scheduler import DigestScheduler

class AutoPM:
    """Main AutoPM application class"""
    
    def __init__(self):
        """Initialize the AutoPM application"""
        self.fetchers = self._initialize_fetchers()
        self.summarizer = OpenAISummarizer()
        self.notifiers = self._initialize_notifiers()
        self.scheduler = DigestScheduler()
    
    def _initialize_fetchers(self) -> Dict[str, Any]:
        """Initialize and configure data fetchers"""
        fetchers = {}
        
        try:
            # Initialize Slack fetcher
            slack_config = {
                "channels": ["#general", "#engineering"],  # Default channels, can be configured
                "lookback_days": 1
            }
            fetchers["slack"] = SlackFetcher(slack_config)
            logger.info("Initialized Slack fetcher")
        except Exception as e:
            logger.warning(f"Could not initialize Slack fetcher: {e}")
        
        try:
            # Initialize Jira fetcher
            jira_config = {
                "projects": [],  # Add project keys here or configure via settings
                "lookback_days": 7
            }
            fetchers["jira"] = JiraFetcher(jira_config)
            logger.info("Initialized Jira fetcher")
        except Exception as e:
            logger.warning(f"Could not initialize Jira fetcher: {e}")
        
        try:
            # Initialize Notion fetcher
            notion_config = {
                "lookback_days": 3
            }
            if settings.NOTION_DATABASE_ID:
                fetchers["notion"] = NotionFetcher(notion_config)
                logger.info("Initialized Notion fetcher")
        except Exception as e:
            logger.warning(f"Could not initialize Notion fetcher: {e}")
        
        return fetchers
    
    def _initialize_notifiers(self) -> Dict[str, Any]:
        """Initialize and configure notifiers"""
        notifiers = {}
        
        try:
            # Initialize Slack notifier
            slack_config = {
                "default_channel": "#autopm-digests"
            }
            notifiers["slack"] = SlackNotifier(slack_config)
            logger.info("Initialized Slack notifier")
        except Exception as e:
            logger.warning(f"Could not initialize Slack notifier: {e}")
        
        try:
            # Initialize Email notifier
            email_config = {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "smtp_username": "your-email@gmail.com",
                "smtp_password": "your-app-password",
                "use_tls": True
            }
            notifiers["email"] = EmailNotifier(email_config)
            logger.info("Initialized Email notifier")
        except Exception as e:
            logger.warning(f"Could not initialize Email notifier: {e}")
        
        return notifiers
    
    async def generate_digest(self) -> str:
        """
        Generate a digest by fetching updates from all sources and summarizing them
        
        Returns:
            str: Formatted digest content
        """
        logger.info("Starting digest generation...")
        
        # Fetch updates from all sources
        all_updates = []
        for source, fetcher in self.fetchers.items():
            try:
                updates = await fetcher.fetch_updates()
                logger.info(f"Fetched {len(updates)} updates from {source}")
                all_updates.extend(updates)
            except Exception as e:
                logger.error(f"Error fetching updates from {source}: {e}", exc_info=True)
        
        # Sort updates by timestamp (newest first)
        all_updates.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Generate summary
        summary = await self.summarizer.summarize(all_updates)
        
        # Format the digest
        digest = summary.to_markdown()
        
        logger.info("Digest generation complete")
        return digest
    
    async def send_digest(self, digest_content: str, notifier_types: List[str] = None) -> Dict[str, Dict]:
        """
        Send the digest using the specified notifiers
        
        Args:
            digest_content: The formatted digest content to send
            notifier_types: List of notifier types to use (default: all available)
            
        Returns:
            Dict containing the results from each notifier
        """
        if notifier_types is None:
            notifier_types = list(self.notifiers.keys())
        
        results = {}
        
        for notifier_type in notifier_types:
            if notifier_type in self.notifiers:
                try:
                    if notifier_type == "slack":
                        result = await self.notifiers[notifier_type].send(
                            content=digest_content,
                            channel="#autopm-digests"
                        )
                    elif notifier_type == "email":
                        result = await self.notifiers[notifier_type].send(
                            content=digest_content,
                            subject=f"AutoPM Digest - {datetime.now().strftime('%Y-%m-%d')}",
                            to_emails=["team@example.com"],
                            is_html=False
                        )
                    else:
                        result = await self.notifiers[notifier_type].send(content=digest_content)
                    
                    results[notifier_type] = {
                        "success": result.success,
                        "message": result.message,
                        "details": result.details
                    }
                    logger.info(f"Sent digest via {notifier_type}: {result.message}")
                except Exception as e:
                    error_msg = f"Error sending digest via {notifier_type}: {str(e)}"
                    logger.error(error_msg, exc_info=True)
                    results[notifier_type] = {
                        "success": False,
                        "message": error_msg,
                        "details": {"error": str(e)}
                    }
        
        return results
    
    async def run_digest_cycle(self, notifier_types: List[str] = None):
        """
        Run a complete digest cycle: generate and send digest
        
        Args:
            notifier_types: List of notifier types to use (default: all available)
        """
        try:
            # Generate the digest
            digest = await self.generate_digest()
            
            # Send the digest
            results = await self.send_digest(digest, notifier_types)
            
            # Log results
            success = all(result["success"] for result in results.values())
            if success:
                logger.info("Digest cycle completed successfully")
            else:
                logger.warning("Digest cycle completed with some failures")
            
            return {"success": success, "results": results}
            
        except Exception as e:
            error_msg = f"Error in digest cycle: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {"success": False, "error": error_msg}
    
    async def schedule_digests(self):
        """Schedule periodic digests"""
        # Schedule daily digests (weekdays at 5 PM)
        await self.scheduler.schedule_digest(
            task_id="daily_digest",
            schedule=settings.DIGEST_SCHEDULE,  # e.g., "0 17 * * 1-5" for weekdays at 5 PM
            task_func=self.run_digest_cycle,
            notifier_types=["slack", "email"]  # Use both Slack and email by default
        )
        
        logger.info("Scheduled periodic digests")
    
    async def run(self):
        """Run the AutoPM application"""
        try:
            # Start the scheduler
            await self.scheduler.start()
            
            # Schedule periodic digests
            await self.schedule_digests()
            
            # Keep the application running
            while True:
                await asyncio.sleep(3600)  # Sleep for an hour
                
        except (KeyboardInterrupt, SystemExit):
            logger.info("Shutting down AutoPM...")
            await self.scheduler.stop()
        except Exception as e:
            logger.error(f"Error in AutoPM: {e}", exc_info=True)
            await self.scheduler.stop()
            raise


async def main():
    """Main entry point for the AutoPM application"""
    # Initialize and run AutoPM
    autopm = AutoPM()
    
    # For testing: Run a digest cycle immediately
    # await autopm.run_digest_cycle()
    
    # For production: Run the scheduler
    await autopm.run()


if __name__ == "__main__":
    asyncio.run(main())
