import os
import yaml

from appdirs import AppDirs
from eventhandler.EventHandler import EventHandler
from infrastructure.KafkaEventConsumer import KafkaEventConsumer
from infrastructure.KafkaEventProducer import KafkaEventProducer


def init_kafka_comm(
        kafka_broker_url: str,
        consumer_topics: list,
        producer_topics: list):
    consumers = [KafkaEventConsumer(kafka_broker_url, top) for top in consumer_topics]
    producer = KafkaEventProducer(kafka_broker_url, producer_topics[0])
    return consumers, producer


def read_config(config_path) -> dict:
    with open(config_path, "r") as ymlfile:
        config = yaml.safe_load(ymlfile)
    kafka_broker_url = config.get("KAFKA_BROKER_URL")
    consumer_topics = list(config.get("IN_TOPIC").keys())
    producer_topics = list(config.get("OUT_TOPIC").keys())
    return kafka_broker_url, consumer_topics, producer_topics


def main():
    dirs = AppDirs("showcase-3d-printer-anomaly-counter")
    config_path = os.path.join(dirs.site_config_dir, "config.yaml")
    config = read_config(config_path=config_path)
    kafka_broker_url, consumer_topics, producer_topics = config

    consumers, producer = init_kafka_comm(
                kafka_broker_url=kafka_broker_url,
                consumer_topics=consumer_topics,
                producer_topics=producer_topics
            )
    eventHandler = EventHandler(return_func=producer.send_msg)
    for consumer in consumers:
        consumer.register_kafka_listener(listener_func=eventHandler.on_event)


if __name__ == "__main__":
    main()
