from typing import Any

from properties_and_methods.base_wrapper import BaseDecorator
from types_extensions import void


class LazyProperty(BaseDecorator):
    """
    A decorator class used for defining *instance* properties_and_methods which should not be evaluated prior to being needed.
    These are not cached.

    Usage:

    >>> @LazyProperty
    >>> def some_property(self) -> int:
    >>>     return 1
    """

    def __get__(self, obj: type, klass: type = None) -> Any:
        if obj is void:
            return
        result = obj.__dict__[self.__name__] = self._func(obj)
        return result


class LazyClassProperty(BaseDecorator):
    """
    A decorator class used for defining *class* properties_and_methods which should not be evaluated prior to
    being needed.
    These are not cached.

    Usage:

    >>> @LazyClassProperty
    >>> def some_property(cls) -> int:
    >>>     return 1
    """

    def __get__(self, obj: type, cls: type) -> Any:
        if cls is void:
            return
        result = self._func(cls)
        setattr(cls, self.__name__, result)
        return result
