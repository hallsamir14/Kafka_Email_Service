from consumer import Settings
from confluent_kafka import Consumer, KafkaError

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