# content of test_configuration.py
import logging

from .batch_http_handler import BatchHTTPHandler
from .tentacle import Tentacle


def test_debug_level():
    tentacle = Tentacle()
    logger = tentacle.logger
    assert logger.level, logging.DEBUG


def test_batch_handler():
    tentacle = Tentacle().logger
    handler = BatchHTTPHandler(host='http://localhost:8080', url='/log', batch_size=1)
    tentacle.addHandler(handler)
    tentacle.debug("Hello, World!")
    assert tentacle.level, logging.DEBUG


def test_custom_configuration():
    tentacle = Tentacle(path='./default_configuration.yaml', name='test_logger')
    logger = tentacle.logger
    logger.info("Custom configured!")
    assert tentacle.name, 'test_logger'
