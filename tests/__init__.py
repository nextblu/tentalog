import unittest
import tentalog
import logging


class TestTentaLog(unittest.TestCase):

    def right_level(self):
        tentalog.setup_logging()
        logger = logging.getLogger('root')
        self.assertEqual(logger.level, logging.DEBUG)