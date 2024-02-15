import os
import smtplib
import markdown2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from faker import Faker
from abc import ABC, abstractmethod

# Load environmental variables
load_dotenv()

# Markdown Converter Interface
class MarkdownConverter(ABC):
    @abstractmethod
    def convert_to_html(self, markdown_path: str) -> str:
        pass

class FileMarkdownConverter(MarkdownConverter):
    def convert_to_html(self, markdown_path: str) -> str:
        try:
            with open(markdown_path, 'r', encoding='utf-8') as file:
                markdown_content = file.read()
                return markdown2.markdown(markdown_content)
        except FileNotFoundError:
            return "File path does not exist."

# Email Sender Interface
class EmailSender(ABC):
    @abstractmethod
    def send_email(self, sender: str, receiver: str, subject: str, html_content: str):
        pass

class MailtrapEmailSender(EmailSender):
    def send_email(self, sender: str, receiver: str, subject: str, html_content: str):
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = receiver
        message["Subject"] = subject
        message.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP("sandbox.smtp.mailtrap.io", int(os.getenv("FAKE_SMTP_PORT"))) as server:
            server.login(os.getenv("FAKE_SMTP_LOGIN_USER"), os.getenv("FAKE_SMTP_LOGIN_PASS"))
            server.sendmail(sender, receiver, message.as_string())

# Application Logic
class EmailApplication:
    def __init__(self, email_sender: EmailSender, markdown_converter: MarkdownConverter):
        self.email_sender = email_sender
        self.markdown_converter = markdown_converter

    def send_markdown_email(self, sender: str, receiver: str, subject: str, markdown_path: str):
        html_content = self.markdown_converter.convert_to_html(markdown_path)
        self.email_sender.send_email(sender, receiver, subject, html_content)

def main():
    email_sender = MailtrapEmailSender()
    markdown_converter = FileMarkdownConverter()
    app = EmailApplication(email_sender, markdown_converter)

    # Example usage
    app.send_markdown_email("mailtrap@jlechner.com", "jll38@njit.edu", "subject", "emails/markdown0.md")

    fake = Faker()
    app.send_markdown_email(fake.email(), fake.email(), fake.sentence(), "emails/markdown1.md")

if __name__ == "__main__":
    main()
