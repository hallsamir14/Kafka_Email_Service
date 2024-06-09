# emailer.py

def send_email(self, subject: str, html_content: str, recipient: str):
    try:
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = self.username
        message['To'] = recipient
        message.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP(self.server, self.port) as server:
            server.starttls()  # Use TLS
            server.login(self.username, self.password)
            server.sendmail(self.username, recipient, message.as_string())
        logging.info(f"Email sent to {recipient}")
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")
        raise
