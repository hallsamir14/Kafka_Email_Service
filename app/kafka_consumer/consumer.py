import json
import logging
import logging.config
from confluent_kafka import Consumer, KafkaError
import signal
import sys
from dotenv import load_dotenv
import os

# Load logging configuration from an external JSON file for better maintainability
with open("logging_config.json", "r") as config_file:
    logging_config = json.load(config_file)
    logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)

# Load environment variables from a .env file
load_dotenv()


class Settings:
    def __init__(self):
        # Load settings from environment variables or use default values
        self.kafka_bootstrap_servers = os.getenv(
            "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
        )  # kafka:9092 when consmer is dockerized
        self.commands_topic = os.getenv("COMMANDS_TOPIC", "kafka_commands")
        self.consumer_group = os.getenv("CONSUMER_GROUP", "my_consumer_group")
        self.auto_offset_reset = os.getenv(
            "AUTO_OFFSET_RESET", "earliest"
        )  # Can be set to 'latest' or 'earliest'

    def check_env_variable(self, var_name, default_value) -> None:
        value = os.getenv(var_name, default_value)
        if value == default_value:
            logger.info(
                f"Environment variable {var_name} not set. Using default value: {default_value}"
            )


settings = Settings()
# Check if the required environment variables are set, otherwise log a warning
settings.check_env_variable("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
settings.check_env_variable("COMMANDS_TOPIC", "kafka_commands")
settings.check_env_variable("CONSUMER_GROUP", "my_consumer_group")
settings.check_env_variable("AUTO_OFFSET_RESET", "earliest")

# Initialize the Kafka Consumer with settings from the `.env` file
consumer = Consumer(
    {
        "bootstrap.servers": settings.kafka_bootstrap_servers,
        "group.id": settings.consumer_group,
        "auto.offset.reset": settings.auto_offset_reset,
    }
)
consumer.subscribe([settings.commands_topic])


def signal_handler(signal, frame):
    """Graceful shutdown of the consumer on receiving SIGINT or SIGTERM."""
    logger.info("Shutting down consumer...")
    consumer.close()
    sys.exit(0)


# Register signal handlers for graceful termination
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def process_message(message):
    """Log the processing of each message."""
    # logger.info(f"Processing message: {message}")
    print(message)  # test output from celery task with passed argument


def consume_messages():
    """Continuously consume messages from Kafka and process them."""
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                # Handle errors such as the end of a partition or other Kafka errors
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.info(
                        f"End of partition reached {msg.topic()}:{msg.partition()}"
                    )
                else:
                    logger.error(f"Error occurred: {msg.error().str()}")
            else:
                # Process the valid message
                message = msg.value().decode("utf-8")
                process_message(json.loads(message))
    except Exception as e:
        logger.error(f"An unexpected exception occurred: {e}")
    finally:
        # Ensure the consumer is properly closed during an unexpected shutdown
        consumer.close()
        logger.info("Consumer closed")


if __name__ == "__main__":
    consume_messages()
