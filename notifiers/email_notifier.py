import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List, Optional

from .base_notifier import BaseNotifier, NotificationResult
from config.settings import settings

logger = logging.getLogger(__name__)

class EmailNotifier(BaseNotifier):
    """Sends notifications via email"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config or {})
        self.smtp_server = self.config.get("smtp_server", "smtp.gmail.com")
        self.smtp_port = self.config.get("smtp_port", 587)
        self.smtp_username = self.config.get("smtp_username", "")
        self.smtp_password = self.config.get("smtp_password", "")
        self.sender_email = self.config.get("sender_email", self.smtp_username)
        self.use_tls = self.config.get("use_tls", True)
    
    async def send(self, content: str, **kwargs) -> NotificationResult:
        """
        Send an email
        
        Args:
            content: The email body (HTML or plain text)
            **kwargs: Additional arguments:
                - subject: Email subject (required)
                - to_emails: List of recipient emails (required)
                - cc_emails: List of CC emails
                - bcc_emails: List of BCC emails
                - is_html: Whether the content is HTML (default: False)
                
        Returns:
            NotificationResult indicating success or failure
        """
        subject = kwargs.get("subject", "AutoPM Digest")
        to_emails = kwargs.get("to_emails", [])
        cc_emails = kwargs.get("cc_emails", [])
        bcc_emails = kwargs.get("bcc_emails", [])
        is_html = kwargs.get("is_html", False)
        
        if not to_emails:
            return NotificationResult(
                success=False,
                message="No recipient emails provided",
                details={"error": "missing_recipients"}
            )
        
        try:
            # Create message container
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = ", ".join(to_emails)
            
            if cc_emails:
                msg['Cc'] = ", ".join(cc_emails)
            
            # All recipients (to + cc + bcc)
            all_recipients = to_emails + cc_emails + bcc_emails
            
            # Attach the content as plain text or HTML
            content_type = 'html' if is_html else 'plain'
            msg.attach(MIMEText(content, content_type, 'utf-8'))
            
            # Connect to the SMTP server and send the email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                
                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)
                
                server.send_message(msg)
            
            return NotificationResult(
                success=True,
                message=f"Email sent to {len(all_recipients)} recipients",
                details={
                    "to": to_emails,
                    "cc": cc_emails,
                    "bcc": bcc_emails,
                    "subject": subject
                }
            )
            
        except smtplib.SMTPException as e:
            error_message = f"SMTP error sending email: {str(e)}"
            logger.error(error_message)
            return NotificationResult(
                success=False,
                message=error_message,
                details={"error": str(e), "smtp_server": self.smtp_server}
            )
        except Exception as e:
            error_message = f"Unexpected error sending email: {str(e)}"
            logger.error(error_message, exc_info=True)
            return NotificationResult(
                success=False,
                message=error_message,
                details={"error": str(e)}
            )
