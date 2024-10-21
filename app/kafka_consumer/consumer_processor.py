import sys
import json
import signal
from consumer_config import Config
from confluent_kafka import Consumer, KafkaError

# Initialize the Config class to load environment variables and set up logging
settings = Config()
logger = settings.set_logger()

# Check if the required environment variables are set, otherwise log a warning
settings.check_env_variable("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
settings.check_env_variable("COMMANDS_TOPIC", "kafka_commands")
settings.check_env_variable("CONSUMER_GROUP", "my_consumer_group")
settings.check_env_variable("AUTO_OFFSET_RESET", "earliest")

# Define the ConsumerProcessor class to process messages from Kafka
class ConsumerProcessor:
    # Initialize the Kafka Consumer with settings from the `.env` file using Config instance
    try:

        consumer = Consumer(
            {
                "bootstrap.servers": settings.kafka_bootstrap_servers,
                "group.id": settings.consumer_group,
                "auto.offset.reset": settings.auto_offset_reset,
            }
        )
        consumer.subscribe([settings.commands_topic])
        logger.info("Kafka consumer initialized and subscribed to topic.")
    except Exception as e:
        logger.error(f"Failed to initialize Kafka consumer: {e}")
        sys.exit(1)
        
    def __init__(self):
        pass

    def __log_message(self, message):
        """Log the processing of each message."""
        logger.info(f"Processing message: {message}")

    
    def __signal_handler(signal, frame, consumer):
        """Graceful shutdown of the consumer on receiving SIGINT or SIGTERM."""
        logger.info("Shutting down consumer...")
        consumer.close()
        sys.exit(0)

    # Register signal handlers for graceful termination
    signal.signal(signal.SIGINT, __signal_handler)
    signal.signal(signal.SIGTERM, __signal_handler)



    def display_messages(self,consumer):
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
                    self.__log_message(json.loads(message))
        except Exception as e:
            logger.error(f"An unexpected exception occurred: {e}")
        finally:
            # Ensure the consumer is properly closed during an unexpected shutdown
            consumer.close()
            logger.info("Consumer closed")


if __name__ == "__main__":
    processor = ConsumerProcessor()
    processor.display_messages(ConsumerProcessor.consumer)
