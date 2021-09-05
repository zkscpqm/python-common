from typing import Callable


class BaseDecorator:
    def __init__(self, wrapped: Callable):
        self._func = wrapped
        self.__name__ = wrapped.__name__
        self.__doc__ = wrapped.__doc__
        wrapped.__wrapped__ = self
