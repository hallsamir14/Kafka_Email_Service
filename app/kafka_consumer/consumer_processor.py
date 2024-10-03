import os
import logging
from confluent_kafka import Consumer, KafkaError

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Settings:
    def __init__(self):
        self.kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.commands_topic = os.getenv('COMMANDS_TOPIC', 'kafka_commands')
        self.consumer_group = os.getenv('CONSUMER_GROUP', 'my_consumer_group')
        self.auto_offset_reset = os.getenv('AUTO_OFFSET_RESET', 'earliest')

    def check_env_variable(self, var_name, default):
        value = os.getenv(var_name, default)
        return value

# Instantiate Settings
settings = Settings()

# Only call this function once
def check_env_with_logging(var_name, default):
    value = settings.check_env_variable(var_name, default)
    if value == default:
        logger.warning(f"Environment variable {var_name} is not set. Using default value: {default}")
    else:
        logger.info(f"Environment variable {var_name} is set: {value}")

check_env_with_logging("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
check_env_with_logging("COMMANDS_TOPIC", "kafka_commands")
check_env_with_logging("CONSUMER_GROUP", "my_consumer_group")
check_env_with_logging("AUTO_OFFSET_RESET", "earliest")

# Initialize the Kafka Consumer
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
    logger.error(f"Failed to initialize Kafka Consumer: {e}")

# Subscribe to the Kafka topic
try:
    consumer.subscribe([settings.commands_topic])
    logger.info(f"Subscribed to Kafka topic: {settings.commands_topic}")
except KafkaError as e:
    logger.error(f"Failed to subscribe to Kafka topic: {e}")
