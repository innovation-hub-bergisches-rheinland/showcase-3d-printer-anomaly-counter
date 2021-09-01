import json
import sys
import threading

from kafka import KafkaConsumer


class KafkaEventConsumer:
    def __init__(self, kafka_broker_url, topic):

        self.kafka_broker_url = kafka_broker_url
        self.topic = topic

    def register_kafka_listener(self, listener_func):
        # Poll kafka
        def poll():
            # Initialize consumer Instance
            consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=[self.kafka_broker_url],
            )
            for msg in consumer:
                data = json.loads(self._decode_msg(msg))
                topic = msg.topic()
                listener_func(data, topic)
        print("About to register listener to topic:", self.topic)
        t1 = threading.Thread(target=poll)
        t1.start()
        print("started a background thread")

    def _decode_msg(self, msg):
        try:
            decoded = msg.value.decode("utf-8")
            return decoded
        except Exception as e:
            print(f"Error decoding data: {repr(e)}")
            sys.exit()
