from functools import wraps

__author__ = 'stas'

class Utils:

    @staticmethod
    def funcKey(func):
        return "{}.{}".format(func.__module__, func.__name__)

    @staticmethod
    def tolist(func):
        @wraps(func)
        def inner(*a, **k):
            return list(func(*a, **k))
        return inner
