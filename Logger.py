
import logging
import os
import datetime
import time

class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(object, metaclass=SingletonType):
    # __metaclass__ = SingletonType   # python 2 Style
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger("crumbs")
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s')

        now = datetime.datetime.now()
        dirname = "./logs"

        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        fileHandler = logging.FileHandler(dirname + "/log_" + now.strftime("%Y-%m-%d")+".log")

        #streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)
        #streamHandler.setFormatter(formatter)

        self._logger.addHandler(fileHandler)
        #self._logger.addHandler(streamHandler)


    def get_logger(self):
        return self._logger

    def info(self, str):
        self._logger.info(str)
    
    def debug(self, str):
        self._logger.debug(str)

