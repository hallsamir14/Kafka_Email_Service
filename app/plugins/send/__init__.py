from app.commands import Command
from app.email_JL.emailer import MailtrapEmailSender, FileMarkdownConverter, EmailApplication

class SendCommand(Command):
    def execute(self):
        sender = input("Sender: ").strip()
        recipient = input("Recipient:").strip()
        subject = input("Subject: ").strip()
        content = "markdowns/markdown0.md"
        email_sender = MailtrapEmailSender()
        markdown_converter = FileMarkdownConverter()
        emailer = EmailApplication(email_sender, markdown_converter)
        emailer.send_markdown_email(sender, recipient, subject, content)
