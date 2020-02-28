import unittest
import tentalog
import logging


class TestTentalog(unittest.TestCase):

    def right_level(self):
        tentalog.setup_logging()
        logger = logging.getLogger('root')
        self.assertEqual(logger.level, logging.DEBUG)


if __name__ == "__main__":
    unittest.main()
