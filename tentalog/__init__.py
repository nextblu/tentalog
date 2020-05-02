import os
import logging.config
import logging
import coloredlogs
import yaml
import requests
from queue import Queue


class Tentacle:

    def __init__(self, path=os.path.join(os.path.dirname(__file__), "default_configuration.yaml"), name='root'):
        self.__name = name
        self.__path = path
        if not os.path.exists(self.__path):
            self.__path = os.path.join(os.path.dirname(__file__), "default_configuration.yaml")
        if not os.path.exists(os.path.join(os.getcwd(), "logs")):
            os.makedirs(os.path.join(os.getcwd(), "logs"))
        with open(self.__path) as file:
            try:
                config = yaml.safe_load(file.read())
                logging.config.dictConfig(config)
                if "loggers" in config:
                    if self.__name in config["loggers"]:
                        self.__logger = logging.getLogger(self.__name)
                        self.__logger.setLevel(config["loggers"][self.__name]["level"])
                    else:
                        self.__logger = logging.getLogger("root")
                        self.__name = "root"
                        self.__logger.warning(f"The name {name} was not found in configuration. "
                                              f"You are currently using the root logger instead.")
                else:
                    self.__logger = logging.getLogger("root")
                    self.__logger.warning("No configured loggers found. You are currently using the root logger.")
                if 'coloredlogs' in config and 'active' in config['coloredlogs']:
                    if 'formatter' in config['coloredlogs']:
                        coloredlogs.install(logger=self.__logger, level=config["loggers"][self.__name]["level"],
                                            fmt=config['formatters'][config['coloredlogs']['formatter']]['format'])
                    else:
                        coloredlogs.install(logger=self.__logger, level=config["loggers"][self.__name]["level"])
            except yaml.YAMLError as e:
                logging.basicConfig(level=logging.DEBUG)
                self.__logger = logging.getLogger(self.__name)
                self.__logger.error("Error in Logging Configuration. Using default configuration", e)
                coloredlogs.install(level=logging.DEBUG)

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    @property
    def logger(self):
        return self.__logger


class BatchHTTPHandler(logging.handlers.HTTPHandler):
    """
    Specialization of the logging.handlers.HTTPHandler that sends requests as JSON and in batch.
    The payload sent by this handler
    will look like
    {
        'data': [
            {
                ...
            },
            {
                ...
            },
            ...
        ]
    }
    """

    def __init__(self, host, url, batch_size=10, method='GET', secure=False, credentials=None, context=None):
        super().__init__(host, url, method=method, secure=secure, credentials=credentials, context=context)
        self.__host = host
        self.__url = url
        self.__batch_size = batch_size
        self.__queue = Queue()
        self.__client = requests.Session()
        self.__client.headers.update({'Content-Type': 'application/json'})

    def emit(self, record):
        try:
            self.__queue.put(record)
            if self.__queue.qsize() > 0 and (self.__queue.qsize() % self.__batch_size) == 0:
                payload = {}
                logs = []
                backup_queue = []
                i = 0
                while not self.__queue.empty():
                    backup_queue.append(self.__queue.get())
                    logs.append(backup_queue[i].__dict__)
                    i += 1
                payload['data'] = logs
                try:
                    self.custom_emit(payload)
                    with self.__queue.mutex:
                        self.__queue.queue.clear()

                    self.flush()
                except:
                    for log in backup_queue:
                        self.__queue.put(log)

        except:
            self.handleError(record)

    def custom_emit(self, logs):
        self.__client.post(self.__host + self.__url, json=logs)

    def __del__(self):
        self.__client.close()
