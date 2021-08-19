from typing import Callable, Any

from types_extensions import void


class LazyProperty:
    """
    A decorator class used for defining *instance* properties which should not be evaluated prior to being needed.
    These are not cached.

    Usage:

    >>> @LazyProperty
    >>> def some_property(self) -> int:
    >>>     return 1
    """

    def __init__(self, func: Callable) -> void:
        self.__func: Callable = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj: type, klass: type = None) -> Any:
        if obj is void:
            return
        result = obj.__dict__[self.__name__] = self.__func(obj)
        return result


class LazyClassProperty:
    """
    A decorator class used for defining *class* properties which should not be evaluated prior to being needed.
    These are not cached.

    Usage:

    >>> @LazyClassProperty
    >>> def some_property(cls) -> int:
    >>>     return 1
    """

    def __init__(self, func: Callable) -> void:
        self.__func: Callable = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj: type, cls: type) -> Any:
        if cls is void:
            return
        result = self.__func(cls)
        setattr(cls, self.__name__, result)
        return result
