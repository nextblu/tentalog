# content of test_configuration.py
from tentalog import Tentacle
import logging


def test_debug_level():
    tentacle = Tentacle()
    logger = tentacle.logger
    assert logger.level, logging.DEBUG


def test_configuration_import():
    tentacle = Tentacle()
    assert (tentacle.path, "/home/runner/work/tentalog/tentalog/default_configuration.yaml")


def test_test():
    tentacle = Tentacle()
    log = tentacle.logger
    assert (True, isinstance(log, Tentacle))
