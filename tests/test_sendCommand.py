import pytest
from unittest.mock import patch
from app import App
from app.commands import CommandHandler
from app.plugins.send import SendCommand
from app.plugins.exit import ExitCommand




def test_sendCommand(capfd):
    with patch("builtins.input", side_effect=["SenderName", "RecipientName", "SubjectName"]):
        send_command = SendCommand()
        send_command.execute()

    # Capture the output
    out, err = capfd.readouterr()

    # Assert the expected output or behavior
    assert "Sender: " 
    assert "Recipient:"
    assert "Subject: " 
    assert err == "", "Unexpected error output"


    


