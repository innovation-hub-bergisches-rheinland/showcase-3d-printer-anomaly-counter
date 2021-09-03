import time
import uuid


class Request():
    def __init__(self, start_timestamp) -> None:
        self.id = str(uuid.uuid4())
        self.start_timestamp = start_timestamp
        self.anomalies = 0
        self.duration = 0
        self.stop_timestamp = None

    def anomaly_detected(self):
        self.anomalies += 1

    def stop_request(self, timestamp=round(time.time() * 1000.0)):
        self.stop_timestamp = timestamp
        self.active = False
        self.duration = self.stop_timestamp - self.start_timestamp
