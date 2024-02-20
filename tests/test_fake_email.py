import pytest
import os
from unittest.mock import patch, MagicMock
from email_JL.emailer import FileMarkdownConverter, MailtrapEmailSender, EmailApplication
from unittest.mock import ANY

#Mocking the SMTP server for MailtrapEmailSender
@patch("email_JL.emailer.smtplib.SMTP")
def test_mailtrap_email_sender(mock_smtp):
    sender = MailtrapEmailSender()
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    sender.send_email("from@example.com", "to@example.com", "Subject", "<p>HTML Content</p>")

    # Verify that SMTP server is called with correct parameters
    mock_smtp.assert_called_with("sandbox.smtp.mailtrap.io", int(os.getenv("FAKE_SMTP_PORT")))
    mock_server.login.assert_called_with(os.getenv("FAKE_SMTP_LOGIN_USER"), os.getenv("FAKE_SMTP_LOGIN_PASS"))
    mock_server.sendmail.assert_called_with("from@example.com", "to@example.com", ANY)


# Integration test for EmailApplication
@patch("email_JL.emailer.FileMarkdownConverter.convert_to_html", return_value="<p>Converted HTML</p>")
@patch("email_JL.emailer.MailtrapEmailSender.send_email")
def test_email_application(mock_send_email, mock_convert_to_html):
    app = EmailApplication(MailtrapEmailSender(), FileMarkdownConverter())
    app.send_markdown_email("from@example.com", "to@example.com", "Subject", "markdowns/markdown2.md")

    mock_convert_to_html.assert_called_once()
    mock_send_email.assert_called_once_with("from@example.com", "to@example.com", "Subject", "<p>Converted HTML</p>")

if __name__ == "__main__":
    pytest.main()