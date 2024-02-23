from app.commands import CommandHandler
from app.commands.send import SendCommand
from app.commands.exit import ExitCommand


class App:
    def __init__(self):  # Constructor
        self.command_handler = CommandHandler()

    def start(self):
        self.command_handler.register_command("send", SendCommand())
        self.command_handler.register_command("exit", ExitCommand())
        print("Type 'exit' to exit.")
        while True:  #REPL Read, Evaluate, Print, Loop
            self.command_handler.execute_command(input(">>> ").strip())