from tentalog import Tentacle
import logging


def Test_level():
    tentacle = Tentacle()
    logger = tentacle.logger
    assert logger.level, logging.DEBUG
