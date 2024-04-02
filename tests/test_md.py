# tests.py
import pytest
from unittest.mock import patch, MagicMock
from app.email_JL.emailer import FileMarkdownConverter, MailtrapEmailSender, EmailApplication

# Test for markdown to HTML conversion
def test_convert_to_html():
    converter = FileMarkdownConverter()
    test_markdown_path = "markdowns/markdown2.md" 
    # Assuming the test_markdown.md file contains "# Title\n\nSome content."
    expected_html = "<h1>Title</h1>\n\n<p>Some content.</p>\n"
    assert converter.convert_to_html(test_markdown_path) == expected_html


if __name__ == "__main__":
    pytest.main()
