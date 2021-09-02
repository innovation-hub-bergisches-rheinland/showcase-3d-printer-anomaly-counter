import re
import time

from showcase_3d_printer_anomaly_counter import __version__
from showcase_3d_printer_anomaly_counter.eventhandler.EventHandler import EventHandler
from showcase_3d_printer_anomaly_counter.eventhandler.request import Request


input_raw_temp0 = {
    "fields": {
        "t_bed_gvn": 60,
        "t_bed_set": 60,
        "t_nozzle_gvn": 215.1,
        "t_nozzle_set": 215,
        "time": 1629198908873
    },
    "tags": {
        "topic": "showcase-3d-printer/prusa-printer/temperature"
    }
}

input_raw_temp1 = {
    "fields": {
        "t_bed_gvn": 0,
        "t_bed_set": 0,
        "t_nozzle_gvn": 0,
        "t_nozzle_set": 0,
        "time": 1629198108873
    },
    "tags": {
        "topic": "showcase-3d-printer/prusa-printer/temperature"
    }}

input_raw_ignore = {
    "tags": {
        "topic": "showcase-3d-printer/prusa-printer/esp32"
    }}


def test_version():
    assert __version__ == '0.1.4'


def test_request_init():
    timestamp = round(time.time() * 1000.0)
    uuid4_re = "[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
    request = Request(timestamp)
    assert re.match(uuid4_re, request.id)
    assert request.start_timestamp == timestamp
    assert request.anomalies == 0
    assert request.duration == 0
    assert request.active is True
    assert request.stop_timestamp is None


def test_request_anomaly_detected():
    timestamp = round(time.time() * 1000.0)
    request = Request(timestamp)
    assert request.anomalies == 0
    request.anomaly_detected()
    assert request.anomalies == 1


def test_request_stop_request():
    timestamp_start = round(time.time() * 1000.0)
    timestamp_stop = round(time.time() * 1000.0) + 200
    request = Request(timestamp_start)
    request.stop_request(timestamp_stop)
    assert request.stop_timestamp == timestamp_stop
    assert request.active is False
    assert request.duration == timestamp_stop - timestamp_start


def test_eventhandler():
    def returntest(request: dict):
        assert type(request) is dict
        uuid4_re = "[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
        assert re.match(uuid4_re, request['id'])
    EventHandler(returntest)


def test_start_new_request():
    class ReturnTest:
        def __init__(self):
            self.return_func_calls = 0
            self.id = None

        def return_func(self, request: dict):
            assert type(request) is dict
            self.return_func_calls += 1
            self.id = request['id']

    returntest = ReturnTest()
    eventhandler = EventHandler(returntest.return_func)
    assert returntest.return_func_calls == 1
    id1 = returntest.id
    eventhandler.on_event(input_raw_temp0, "showcase-3d-printer_prusa-esp32")
    assert returntest.return_func_calls == 1
    assert eventhandler.temp == input_raw_temp0["fields"]["t_nozzle_set"]
    assert id1 == returntest.id
    eventhandler.on_event(input_raw_temp1, "showcase-3d-printer_prusa-esp32")
    assert id1 != returntest.id
    assert returntest.return_func_calls == 3


def test_handly_anomaly_data():
    class ReturnTest:
        def __init__(self):
            self.return_func_calls = 0
            self.induced_anomalies = 0

        def return_func(self, request: dict):
            assert type(request) is dict
            assert request['anomalies'] == self.induced_anomalies
            self.return_func_calls += 1

    returntest = ReturnTest()
    eventhandler = EventHandler(returntest.return_func)

    returntest.induced_anomalies += 1
    eventhandler.on_event({}, "ender_printer_anomalies")
    assert returntest.return_func_calls == 2
