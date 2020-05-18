# content of test_configuration.py
from tentalog import Tentacle
import logging


def test_debug_level():
    tentacle = Tentacle()
    logger = tentacle.logger
    assert logger.level, logging.DEBUG
