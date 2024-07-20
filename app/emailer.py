from builtins import Exception, int, str
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import sys
from dotenv import load_dotenv
import os

load_dotenv()
sys.path.append(os.getenv('PROJECT_PARENT_DIR',''))
from app.utils.SMTP_connection import smtp_Settings
from app.utils.template_manager import TemplateManager
class emailer():

    @staticmethod
    def send_email(subject: str, html_content: str, recipient: str):
        settings = smtp_Settings()
        try:
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = settings.username
            message['To'] = recipient
            message.attach(MIMEText(html_content, 'html'))

            with smtplib.SMTP(settings.server, settings.port) as server:
                server.starttls()  # Use TLS
                server.login(settings.username, settings.password)
                server.sendmail(settings.username, recipient, message.as_string())
            logging.info(f"Email sent to {recipient}")
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
            raise

'''
In this code, we first create an instance of the `emailer` class (`emailer_instance`), 
and then call the `send_email` method on this instance.
'''
TemplateManager = TemplateManager()

content:str = TemplateManager.render_template('email_verification', name='John Doe', verification_url='http://example.com/verify/1234')
emailer.send_email('content',content,'recipient')