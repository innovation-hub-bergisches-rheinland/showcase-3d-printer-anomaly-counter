import time
import traceback

from .request import Request


class EventHandler:

    def __init__(self, return_func):
        self.return_func = return_func
        self.request = Request(round(time.time() * 1000.0))
        self.is_request_active = False

    def on_event(self, event: dict, kafka_topic: str):
        try:
            if kafka_topic == "showcase-3d-printer_prusa-esp32":
                self._handle_raw_data(event)
            elif kafka_topic == "ender_printer_anomalies":
                self._handle_anomaly_data()
        except Exception as e:
            traceback.print_tb(e)

    def _handle_raw_data(self, event: dict):
        if event['tags']['topic'] == "showcase-3d-printer/prusa-printer/temperature":
            self._handle_raw_temperature_data(event['fields'])

    def _handle_anomaly_data(self):
        if self.is_request_active:
            self.request.anomaly_detected()
            self.return_func(self.request.__dict__)

    def _handle_raw_temperature_data(self, fields: dict):
        if fields['t_nozzle_set'] > 0 and not self.is_request_active:
            self._start_new_request(fields['time'])
        elif fields['t_nozzle_set'] == 0 and self.is_request_active:
            self._stop_request(fields['time'])

    def _start_new_request(self, timestamp: int):
        self.is_request_active = True
        self.request = Request(timestamp)
        self.return_func(self.request.__dict__)

    def _stop_request(self, timestamp: int):
        self.is_request_active = False
        self.request.stop_request(timestamp)
        self.return_func(self.request.__dict__)
