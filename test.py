import unittest
import logging
from tentalog import Tentacle


class TestTentalog(unittest.TestCase):

    def test_level(self):
        tentacle = Tentacle()
        logger = tentacle.logger
        self.assertEqual(logger.level, logging.DEBUG)


if __name__ == "__main__":
    unittest.main()
