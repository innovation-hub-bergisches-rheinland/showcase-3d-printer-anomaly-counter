import time
import traceback

from request import Request


class EventHandler:

    def __init__(self, return_func):
        self.return_func = return_func
        self.request = Request(round(time.time() * 1000.0))
        self.return_func(self.request)
        self.temp = None

    def on_event(self, event: dict, topic: str):
        try:
            if topic == "showcase-3d-printer_prusa-esp32":
                self._handle_raw_data(event)
            elif topic == "ender_printer_anomalies":
                self._handle_anomaly_data(event)
        except Exception as e:
            traceback.print_tb(e)

    def _handle_raw_data(self, event: dict):
        if event['tags']['topic'] == "showcase-3d-printer/prusa-printer/temperature":
            self._handle_raw_temperature_data(event['fields'])

    def _handle_anomaly_data(self, event: dict):
        self.request.anomaly_detected()
        self.return_func(self.request)

    def _handle_raw_temperature_data(self, fields: dict):
        if not self.temp:
            self.temp = fields['t_nozzle_set']
        elif self.temp != fields['t_nozzle_set']:
            self._start_new_request(fields['time'])

    def _start_new_request(self, timestamp: int):
        self.request.stop_request(timestamp)
        self.return_func(self.request)
        self.request = Request(timestamp)
        self.return_func(self.request)
