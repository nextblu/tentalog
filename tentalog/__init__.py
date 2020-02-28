import os
import logging.config
import logging
import coloredlogs
import yaml


class Tentacle:

    def __init__(self, path, name='root'):
        self.__name = name
        if path:
            self.__path = path
        if not self.__path or not os.path.exists(self.__path):
            self.__path = "default_configuration.yaml"
            if not os.path.exists(os.path.join(os.getcwd(), "logs")):
                os.makedirs(os.path.join(os.getcwd(), "logs"))
        with open(self.__path) as file:
            try:
                config = yaml.safe_load(file.read())
                logging.config.dictConfig(config)
                if self.__name in config["loggers"]:
                    self.__logger = logging.getLogger(self.__name)
                else:
                    self.__logger = logging.getLogger("root")
                    self.__logger.warning(f"The name {name} was not found in configuration. "
                                          f"You are currently using the root logger instead.")
            except yaml.YAMLError as e:
                logging.basicConfig(level=logging.DEBUG)
                self.__logger = logging.getLogger(self.__name)
                self.__logger.error("Error in Logging Configuration. Using default configuration", e)
                coloredlogs.install(level=logging.DEBUG, logger=logger)

    @property
    def name(self):
        return self.__name
    
    @property
    def path(self):
        return self.__path

    @property
    def logger(self):
        return self.__logger


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
