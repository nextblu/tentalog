import requests
import logging
from queue import Queue


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
                print(payload)
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
