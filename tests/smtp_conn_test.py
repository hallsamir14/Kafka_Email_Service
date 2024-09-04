import pytest
import os
import sys
import smtplib

# Get the directory of the current script (test file)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (project root)
project_root = os.path.dirname(current_dir)

# Add the project root to the Python path
sys.path.append(project_root)

from app.utils.SMTP_connection import smtp_Settings

class TestSMTP():
    @pytest.fixture
    def settings(self):
        settings = smtp_Settings()
        return settings
    
    def test_server_name(self, settings): 
        result = bool(settings.server and settings.server.strip())
        assert result == True
    
    def test_server_port(self, settings):
        result = isinstance(settings.port, int)
        assert result == True

    def test_server_username(self, settings):
        result = bool(settings.username and settings.username.strip())
        assert result == True

    def test_server_password(self, settings):
        result = bool(settings.password and settings.password.strip())
        assert result == True

    def test_smtp_connection(self, settings):
        server = smtplib.SMTP(settings.server, settings.port)
        server.starttls()

        connection = server.noop()[0]

        assert connection == 250
        server.quit()
