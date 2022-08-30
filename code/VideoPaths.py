

class VideoPaths(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(VideoPaths, cls).__new__(cls)
        return cls.instance

singleton = VideoPaths()