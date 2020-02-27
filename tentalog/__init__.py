import os
import logging.config
import logging
import coloredlogs
import yaml

try:
    from importlib import resources as res
except ImportError:
    import importlib_resources as res

logger = None


def setup(path="default_logging.yaml"):
    global logger
    if not os.path.exists(path):
        path = os.path.join(os.path.dirname(__file__), "default_configuration.yaml")
    if not os.path.exists(os.path.join(os.getcwd(), "logs")):
        os.makedirs(os.path.join(os.getcwd(), "logs"))
    with open(path) as f:
        try:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            logger = logging.getLogger('root')
            if 'coloredlogs' in config and 'active' in config['coloredlogs']:
                if 'formatter' in config['coloredlogs']:
                    print(f'{config["formatters"][config["coloredlogs"]["formatter"]]["format"]}')
                    coloredlogs.install(logger=logger,
                                        fmt=config['formatters'][config['coloredlogs']['formatter']]['format'])
                else:
                    coloredlogs.install(logger=logger)

        except Exception as e:
            logging.basicConfig(level=logging.DEBUG)
            logger = logging.getLogger('root')
            logger.error("Error in Logging Configuration. Using default configuration", e)
            coloredlogs.install(level=logging.DEBUG, logger=logger)


def get_logger():
    return logger
