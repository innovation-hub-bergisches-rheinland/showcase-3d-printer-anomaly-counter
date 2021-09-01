import os
import yaml

from appdirs import AppDirs
from eventhandler.EventHandler import EventHandler
from infrastructure.KafkaEventConsumer import KafkaEventConsumer
from infrastructure.KafkaEventProducer import KafkaEventProducer


def init_kafka_comm(kafka_config):
    kafka_broker_url = kafka_config.get("KAFKA_BROKER_URL")
    consumer_topic = kafka_config.get("IN_TOPIC")
    producer_topic = kafka_config.get("OUT_TOPIC")
    consumer = KafkaEventConsumer(kafka_broker_url, consumer_topic)
    producer = KafkaEventProducer(kafka_broker_url, producer_topic)
    return consumer, producer


def read_config(config_path) -> dict:
    with open(config_path, "r") as ymlfile:
        config = yaml.safe_load(ymlfile)
    return config


def main():
    dirs = AppDirs("pythongenericmodule")
    config_path = os.path.join(dirs.site_config_dir, "config.yaml")
    config = read_config(config_path=config_path)

    consumer, producer = init_kafka_comm(kafka_config=config.get("kafka"))
    eventHandler = EventHandler(return_func=producer.send_msg)
    consumer.register_kafka_listener(listener_func=eventHandler.on_event)


if __name__ == "__main__":
    main()
