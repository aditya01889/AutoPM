import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable, Coroutine
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config.settings import settings

logger = logging.getLogger(__name__)


class DigestScheduler:
    """Schedules and manages periodic digest generation and distribution"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone(settings.TIMEZONE))
        self.jobs = {}
    
    async def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Digest scheduler started")
    
    async def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Digest scheduler stopped")
    
    def schedule_digest(
        self,
        task_id: str,
        schedule: str,
        task_func: Callable[..., Coroutine],
        *args,
        **kwargs
    ) -> bool:
        """
        Schedule a digest task to run at the specified interval
        
        Args:
            task_id: Unique identifier for the task
            schedule: Cron-style schedule string (e.g., "0 17 * * 1-5" for weekdays at 5 PM)
            task_func: Async function to call when the task runs
            *args: Positional arguments to pass to the task function
            **kwargs: Keyword arguments to pass to the task function
            
        Returns:
            bool: True if scheduling was successful, False otherwise
        """
        try:
            # Remove existing job with the same ID if it exists
            self.unschedule_digest(task_id)
            
            # Add the new job
            job = self.scheduler.add_job(
                task_func,
                CronTrigger.from_crontab(schedule),
                args=args,
                kwargs=kwargs,
                id=task_id,
                replace_existing=True,
                max_instances=1,
                misfire_grace_time=300  # 5 minutes grace time
            )
            
            self.jobs[task_id] = job
            next_run = job.next_run_time.astimezone(pytz.timezone(settings.TIMEZONE)) if job.next_run_time else "Not scheduled"
            
            logger.info(
                f"Scheduled digest task '{task_id}' with schedule '{schedule}'. "
                f"Next run: {next_run}"
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling digest task '{task_id}': {str(e)}", exc_info=True)
            return False
    
    def unschedule_digest(self, task_id: str) -> bool:
        """
        Unschedule a digest task
        
        Args:
            task_id: ID of the task to unschedule
            
        Returns:
            bool: True if task was found and removed, False otherwise
        """
        if task_id in self.jobs:
            self.scheduler.remove_job(task_id)
            del self.jobs[task_id]
            logger.info(f"Unscheduled digest task '{task_id}'")
            return True
        return False
    
    def get_scheduled_tasks(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all scheduled tasks
        
        Returns:
            Dict mapping task IDs to task information
        """
        tasks = {}
        for job_id, job in self.jobs.items():
            tasks[job_id] = {
                "next_run_time": job.next_run_time.astimezone(pytz.timezone(settings.TIMEZONE)) if job.next_run_time else None,
                "trigger": str(job.trigger),
                "pending": job.pending
            }
        return tasks
    
    async def trigger_digest_now(self, task_id: str) -> bool:
        """
        Trigger a digest task to run immediately
        
        Args:
            task_id: ID of the task to trigger
            
        Returns:
            bool: True if task was found and triggered, False otherwise
        """
        if task_id in self.jobs:
            job = self.jobs[task_id]
            job.modify(next_run_time=datetime.now(pytz.timezone(settings.TIMEZONE)))
            logger.info(f"Triggered immediate run of digest task '{task_id}'")
            return True
        return False
