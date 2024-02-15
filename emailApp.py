import os
import smtplib
import markdown2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from faker import Faker

# load enviornmental references
load_dotenv()


# Function to convert markdown to HTML------------------------------
def md_to_html(filePath: str) -> str:
    try:
        with open(filePath, 'r', encoding='utf-8') as file:

            # read markdown
            markdown_content: str = file.read()

            # Convert markdoown to html
            html_content: str = markdown2.markdown(markdown_content)

            return html_content
    except FileNotFoundError:
        return (f"File path does not exist.")


# Send directly to mailtrap fake SMTP-----------------------------------
def send_mailTrap_email(sender: str, reciever: str, subject: str, markdown_path: str) -> None:

    sender_addr: str = sender
    receiver_addr: str = reciever
    subject_line: str = subject
    # Store contents of markdown
    markdown_text: str = md_to_html(markdown_path)

    # HTML data
    html_content = """

      {} 
  """.format(markdown_text)  # string formatting to add contents from markdown

    # MIME message variables
    message = MIMEMultipart()
    message["From"] = sender_addr
    message["To"] = receiver_addr
    message["Subject"] = subject_line

    # Attach the HTML content
    message.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", int(os.getenv("FAKE_SMTP_PORT"))) as server:
        server.login(os.getenv("FAKE_SMTP_LOGIN_USER"),
                     os.getenv("FAKE_SMTP_LOGIN_PASS"))
        server.sendmail(sender_addr, receiver_addr, message.as_string())
        
    # Print markdown raw content to user output
    print(markdown_text)

# Send to real email inbox------------------------------------------------


def send_email(sender: str, reciever: str, subject: str, markdown_path: str) -> None:

    sender_addr: str = sender
    receiver_addr: str = reciever
    subject_line: str = subject
    # Store contents of markdown
    markdown_text: str = md_to_html(markdown_path)

    # HTML data
    html_content = """

      {} 
  """.format(markdown_text)  # string formatting to add contents from markdown

    # MIME message variables
    message = MIMEMultipart()
    message["From"] = sender_addr
    message["To"] = receiver_addr
    message["Subject"] = subject_line

    # Attach the HTML content
    message.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP("live.smtp.mailtrap.io", int(os.getenv("SMTP_PORT"))) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("api", os.getenv("SERVER_PASS"))
        server.sendmail(sender_addr, receiver_addr, message.as_string())
    # Print markdown raw content to user output
    print("Sent:" + markdown_text)


def main():
    # send email 1 to mailtrap inbox
    send_mailTrap_email("mailtrap@jlechner.com", "jll38@njit.edu",
               "subject", "emails/markdown0.md")
    # send email2 to mailtrap inbox using faker
    fake = Faker()
    send_mailTrap_email(fake.email(),fake.email(),fake.sentence(),"emails/markdown1.md")


if __name__ == "__main__":
    main()
