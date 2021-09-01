import re
import time

from showcase_3d_printer_anomaly_counter import __version__
from showcase_3d_printer_anomaly_counter.eventhandler.request import Request


def test_version():
    assert __version__ == '0.1.1'


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
