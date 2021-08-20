from typing import Any

from properties_and_methods.base_wrapper import BaseDecorator
from types_extensions import void


class CachedProperty(BaseDecorator):
    """
    A decorator class used for defining *instance* properties_and_methods which should not be evaluated prior to being needed.
    These are not cached.

    Usage:

    >>> @CachedProperty
    >>> def some_property(self) -> int:
    >>>     return 1
    """

    def __get__(self, obj: type, klass: type = None) -> Any:
        if obj is void:
            return
        if self.__name__ in obj.__dict__:
            return obj.__dict__.get(self.__name__)
        result = obj.__dict__[self.__name__] = self.__func(obj)
        return result


class CachedClassProperty(BaseDecorator):
    """
    A decorator class used for defining *class* properties_and_methods which should not be evaluated prior to being needed.
    These are not cached.

    Usage:

    >>> @CachedClassProperty
    >>> def some_property(cls) -> int:
    >>>     return 1
    """

    def __get__(self, obj: type, cls: type) -> Any:
        if cls is void:
            return
        if hasattr(cls, self.__name__):
            return getattr(cls, self.__name__)
        result = self.__func(cls)
        setattr(cls, self.__name__, result)
        return result
