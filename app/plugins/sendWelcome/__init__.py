from app.commands import Command
from app.email_JL.emailer import MailtrapEmailSender, FileMarkdownConverter, EmailApplication
from app.jwt_decoder.decoder import readUser

class sendWelcomeCommand(Command):

    def get_email(self) -> str:
        decoded_token = readUser('app/jwt_decoder/token.txt')
        # Extract email and email verification status from the decoded JWT
        email = decoded_token['token']['email']
        email_verified = decoded_token['token']['email_verified']

        if not email_verified:
            raise ValueError("Email is not verified")

        return email

    def execute(self):
        sender = input("Sender: ").strip()
        recipient = self.get_email()
        subject = input("Subject: ").strip()
        content = "markdowns/welcomeMarkdown.md"
        email_sender = MailtrapEmailSender()
        markdown_converter = FileMarkdownConverter()
        emailer = EmailApplication(email_sender, markdown_converter)
        emailer.send_markdown_email(sender, recipient, subject, content)
