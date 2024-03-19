from emailer import MailtrapEmailSender, FileMarkdownConverter, EmailApplication
from faker import Faker

def main():
    email_sender = MailtrapEmailSender()
    markdown_converter = FileMarkdownConverter()
    app = EmailApplication(email_sender, markdown_converter)

    
    # Example usage
    app.send_markdown_email("mailtrap@jlechner.com", "jll38@njit.edu", "subject", "markdowns/markdown0.md")

    fake = Faker()
    app.send_markdown_email(fake.email(), fake.email(), fake.sentence(), "markdowns/markdown1.md")

if __name__ == "__main__":
    main()