# content of test_configuration.py
from tentacle import Tentacle
from batch_http_handler import BatchHTTPHandler
import logging


def test_debug_level():
    tentacle = Tentacle()
    logger = tentacle.logger
    assert logger.level, logging.DEBUG

def test_batch_handler():
    tentacle = Tentacle().logger
    handl = BatchHTTPHandler(host='http://localhost:8080', url='/log', batch_size=1)
    tentacle.addHandler(handl)
    tentacle.debug("Hello, World!")

test_batch_handler()