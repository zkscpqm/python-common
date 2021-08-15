from typing import Callable, Any

from types_extensions import void


class LazyProperty:

    def __init__(self, func: Callable) -> void:
        self.__func: Callable = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj: type, klass: type = void) -> Any:
        if obj is void:
            return
        result = obj.__dict__[self.__name__] = self.__func(obj)
        return result


class LazyClassProperty:

    def __init__(self, func: Callable) -> void:
        self.__func: Callable = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj: type, cls: type) -> Any:
        if cls is void:
            return void
        result = self.__func(cls)
        setattr(cls, self.__name__, result)
        return result
