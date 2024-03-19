import pkgutil
import importlib
import os
from app.commands import CommandHandler
from app.commands import Command
import logging
import logging.config
import sys


class App:
    def __init__(self):  # Constructor
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        self.command_handler = CommandHandler()

    def configure_logging(self):
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")

    def load_plugins(self):
        # Dynamically load all plugins in the plugins directory
        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.','/')
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_package.replace('.', '/')]):
            if not os.path.exists(plugins_path):
                logging.warning(f"Plugins directory '{plugins_path}' not found.")
                return
            if is_pkg:  # Ensure it's a package
                plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                for item_name in dir(plugin_module):
                    item = getattr(plugin_module, item_name)
                    try:
                        if issubclass(item, (Command)):  # Assuming a BaseCommand class exists
                            self.command_handler.register_command(plugin_name, item())
                            logging.info("Avalailable command: " + plugin_name)
                    except TypeError:
                        continue  # If item is not a class or unrelated class, just ignore

    def start(self):
        # Register commands here
        self.load_plugins()
        logging.info("Application started. Type 'exit' to exit.")
        while True:  #REPL Read, Evaluate, Print, Loop
            self.command_handler.execute_command(input(">>> ").strip())
    