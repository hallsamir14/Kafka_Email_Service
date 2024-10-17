import sys
import json
import signal
from consumer_config import Config
from confluent_kafka import Consumer, KafkaError
from datetime import datetime

# Configure logging to display messages at the INFO level or higher,
# including timestamps and log levels for better traceability.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define a Settings class to encapsulate and manage Kafka-related environment variables.
class Settings:
    def __init__(self):
        # Load environment variables with default values for Kafka configuration.
        self.kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.commands_topic = os.getenv('COMMANDS_TOPIC', 'kafka_commands')
        self.consumer_group = os.getenv('CONSUMER_GROUP', 'my_consumer_group')
        self.auto_offset_reset = os.getenv('AUTO_OFFSET_RESET', 'earliest')

    def check_env_variable(self, var_name, default):
        # Retrieve the value of the specified environment variable, returning a default if not set.
        value = os.getenv(var_name, default)
        return value

# Create an instance of the Settings class to access the configuration.
settings = Settings()

def check_env_with_logging(var_name, default):
    # Check the environment variable and log its value or a warning if the default is used.
    value = settings.check_env_variable(var_name, default)
    if value == default:
        logger.warning(f"Environment variable {var_name} is not set. Using default value: {default}")
    else:
        logger.info(f"Environment variable {var_name} is set: {value}")

# Log the status of critical environment variables related to Kafka configuration.
check_env_with_logging("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
check_env_with_logging("COMMANDS_TOPIC", "kafka_commands")
check_env_with_logging("CONSUMER_GROUP", "my_consumer_group")
check_env_with_logging("AUTO_OFFSET_RESET", "earliest")

# Attempt to initialize the Kafka Consumer with the specified configurations.
try:

    consumer = Consumer(
        {
            "bootstrap.servers": settings.kafka_bootstrap_servers,  # Kafka server(s) to connect to.
            "group.id": settings.consumer_group,  # Consumer group ID for tracking offsets.
            "auto.offset.reset": settings.auto_offset_reset,  # Behavior when no previous offsets exist.
        }
    )
    logger.info("Kafka Consumer initialized successfully.")
except KafkaError as e:
    logger.error(f"Failed to initialize Kafka Consumer: {e}")

# Subscribe to the designated Kafka topic to begin message consumption.
try:
    consumer.subscribe([settings.commands_topic])  # Subscribe to the commands topic.
    logger.info(f"Subscribed to Kafka topic: {settings.commands_topic}")
except KafkaError as e:
    logger.error(f"Failed to subscribe to Kafka topic: {e}")

# Initialize variables to track the timestamps of the first and last messages received.
first_message_time = None
last_message_time = None
message_count = 0
max_messages = 10  # Set a limit on the number of messages to consume for testing.

# Define a function to consume messages and log the time difference between the first and last received messages.
def consume_messages():
    global first_message_time, last_message_time, message_count
    while message_count < max_messages:  # Loop until the maximum message count is reached.
        msg = consumer.poll(1.0)  # Poll for a message with a 1-second timeout.
        
        if msg is None:
            continue  # Skip iteration if no message is received.
        
        if msg.error():  # Check for message errors.
            if msg.error().code() == KafkaError._PARTITION_EOF:
                logger.info(f"End of partition reached {msg.partition()}")  # Log when the end of the partition is reached.
            else:
                logger.error(f"Error in message consumption: {msg.error()}")  # Log any other errors encountered.
            continue

        # Process the received message and increment the message count.
        message_count += 1
        current_time = datetime.now()  # Get the current timestamp.
        logger.info(f"Received message {message_count} at {current_time}: {msg.value().decode('utf-8')}")  # Log the message details.

        # Record the time of the first message received.
        if first_message_time is None:
            first_message_time = current_time

        # Update the time of the last message received.
        last_message_time = current_time

    # Calculate and log the time difference between the first and last messages consumed.
    if first_message_time and last_message_time:
        time_diff = last_message_time - first_message_time
        logger.info(f"Time difference between first and last message: {time_diff}")

# Start the message consumption process 
# (the process of receiving messages from a 
# specified destination using a message consumer object).
try:
    consume_messages()  # Call the function to begin consuming messages.
finally:
    consumer.close()  # Ensure the consumer is properly closed after consumption.
    logger.info("Kafka Consumer closed.")
