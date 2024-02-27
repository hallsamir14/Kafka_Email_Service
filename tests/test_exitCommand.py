import pytest
import unittest
from unittest.mock import patch
from app import App
from app.commands import CommandHandler
from app.plugins.send import SendCommand
from app.plugins.exit import ExitCommand

class TestExitCommand(unittest.TestCase):

    @patch('sys.exit')
    def test_execute(self, mock_sys_exit):
        exit_command = ExitCommand()

        # Call the execute method
        exit_command.execute()

        # Assert that sys.exit was called with the expected argument
        mock_sys_exit.assert_called_once_with("Exiting...")

if __name__ == '__main__':
    unittest.main()
