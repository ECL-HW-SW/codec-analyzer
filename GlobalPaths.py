import json

class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class GlobalPaths(object, metaclass=SingletonType):
        
    _path = None

    def __init__(self, json_path):
        fp = open(json_path, 'r')
        self.__paths = json.load(fp)
        fp.close()

    def get_instance(self):
        return self._path

    def get_paths(self):
        return self.__paths