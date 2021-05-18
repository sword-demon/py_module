from threading import RLock


class Singleton:
    lock = RLock()

    instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.instance:
            return cls.instance
        with cls.lock:
            if cls.instance:
                return cls.instance
            cls.instance = cls.__new__(cls)
            return cls.instance
