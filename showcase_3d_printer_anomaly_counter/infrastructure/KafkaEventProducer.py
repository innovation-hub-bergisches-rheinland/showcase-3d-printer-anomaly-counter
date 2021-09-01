import json
import traceback

from kafka import KafkaProducer


class KafkaEventProducer:
    def __init__(self, kafka_broker_url, topic):

        self.kafka_broker_url = kafka_broker_url
        self.topic = topic

        self.producer = KafkaProducer(
            linger_ms=50,
            bootstrap_servers=[self.kafka_broker_url]
        )

    def send_msg(self, data: dict, partition=0):
        try:
            self.producer.send(self.topic, json.dumps(data).encode('utf-8'))
        except Exception as e:
            print(f"Error sending data to Kafka: {repr(e)}")
            traceback.print_exc()
