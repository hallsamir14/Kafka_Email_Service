import os
import logging
from confluent_kafka import Consumer, KafkaError

# Set up logging configuration to log events at the INFO level or higher 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# create a logger object for logging events
logger = logging.getLogger(__name__) 

# define a settings class to hold the environment variables
class Settings:
    def __init__(self):
        # load kafka configuration from environment variables or set to default if not available
        self.kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.commands_topic = os.getenv('COMMANDS_TOPIC', 'kafka_commands')
        self.consumer_group = os.getenv('CONSUMER_GROUP', 'my_consumer_group')
        self.auto_offset_reset = os.getenv('AUTO_OFFSET_RESET', 'earliest')

    # Helper function to check if environment variable is set, otherwise returns a default value
    def check_env_variable(self, var_name, default):
        value = os.getenv(var_name, default)
        return value

# Instantiate Settings object to access configuration values
settings = Settings()

# Function to log whether an environment variable is set or if the default value is being use 
# Only call this funciton once
def check_env_with_logging(var_name, default):
    value = settings.check_env_variable(var_name, default)
    # log a warning if the environment variable is not set, otherwise log that it's set
    if value == default:
        logger.warning(f"Environment variable {var_name} is not set. Using default value: {default}")
    else:
        logger.info(f"Environment variable {var_name} is set: {value}")

# check and log environment variables related to kafka configuration
check_env_with_logging("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
check_env_with_logging("COMMANDS_TOPIC", "kafka_commands")
check_env_with_logging("CONSUMER_GROUP", "my_consumer_group")
check_env_with_logging("AUTO_OFFSET_RESET", "earliest")

# Try to Initialize the Kafka Consumer with the provied settings
try:
    consumer = Consumer(
        {
            "bootstrap.servers": settings.kafka_bootstrap_servers,
            "group.id": settings.consumer_group,
            "auto.offset.reset": settings.auto_offset_reset,
        }
    )
    logger.info("Kafka Consumer initialized successfully.")
except KafkaError as e:
    # log an error if there's a problem with initializing the kafka consumer
    logger.error(f"Failed to initialize Kafka Consumer: {e}")

# Try to Subscribe to the specified Kafka topic
try:
    consumer.subscribe([settings.commands_topic])
    logger.info(f"Subscribed to Kafka topic: {settings.commands_topic}")
except KafkaError as e:
    logger.error(f"Failed to subscribe to Kafka topic: {e}")
