import json
import os

from appdirs import AppDirs
from kafka import KafkaProducer

from kafka_pc.KafkaPC import KafkaPC
from request import Request


def send_message(producer, kafka_pc, data):
    try:
        producer.send(kafka_pc.out_topic[0], data, partition=0)
    except Exception as e:
        print(f"Error sending data to Kafka: {repr(e)}")


def main():
    dirs = AppDirs("showcase-3d-printer-anomaly-counter")

    config_path = os.path.join(dirs.site_config_dir, "config.yaml")
    config_section = "General, anomaly_counter"

    kafka_pc = KafkaPC(config_path, config_section)
    producer = KafkaProducer(
        linger_ms=50,
        bootstrap_servers=[kafka_pc.config["KAFKA_BROKER_URL"]],
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )

    printing = False
    request = None
    set_temperature_field_key = kafka_pc.config["SET_TEMPERATURE_FIELD_KEY"]

    for msg in kafka_pc.consumer:
        try:
            data = json.loads(kafka_pc.decode_msg(msg))
            if msg.topic() == kafka_pc.config["RAW_DATA_TOPIC"]:
                printing = data[kafka_pc.config[""]]
                if (data["tags"]["TEMPERATURE_SOURCE_TAG_KEY"]
                        == kafka_pc.config["TEMPERATURE_SOURCE_TAG_VALUE"]):
                    if (printing is False
                            and data["fields"][set_temperature_field_key] > 0):
                        printing = True
                        request = Request(data["fields"]["time"])
                        send_message(producer, kafka_pc, data=request.toJSON())
                    elif (printing is True
                            and data["fields"][set_temperature_field_key] == 0):
                        printing = False
                        request.stop_request(data["fields"]["time"])
                        send_message(producer, kafka_pc, data=request.toJSON())
            elif msg.topic() == kafka_pc.config["ANOMALY_TOPIC"] and printing is True:
                request.anomaly_detected()
                send_message(producer, kafka_pc, request.toJSON())
        except ValueError as ve:
            print(f"Could not parse input: {repr(ve)}")


if __name__ == "__main__":
    main()
