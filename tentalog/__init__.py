import os
import logging.config
import logging
import coloredlogs
import yaml


def setup_logging(path='default_logging.yaml', level=logging.INFO):
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                print('Error in Logging Configuration. Using default configuration')
                print(e)
                logging.basicConfig(level=level)
                coloredlogs.install(level=level)
    else:
        print('Using default configuration.')
        logging.basicConfig(level=level)
        coloredlogs.install(level=level)

setup_logging()