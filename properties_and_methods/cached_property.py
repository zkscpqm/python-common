from typing import Any, Callable

from meta.singleton_meta import SingletonMeta
from properties_and_methods.base_wrapper import BaseDecorator
from types_extensions import void


class CachedProperty(BaseDecorator):
    """
    A decorator class used for defining *instance* properties_and_methods which should not be evaluated prior to being
    needed.
    These are not cached.

    Usage:

    >>> @CachedProperty
    >>> def some_property(self) -> int:
    >>>     return 1
    """

    class _Missing(metaclass=SingletonMeta):
        # To distinguish None returnvalue vs missing cached var
        ...

    def __init__(self, wrapped: Callable) -> void:
        super().__init__(wrapped)
        self.cached_var: Any = self._Missing()

    @staticmethod
    def build_invalidate_method_name(property_name: str) -> str:
        return f'invalidate_cached_property_{property_name}'

    def __get__(self, obj: type, klass: type = None) -> Any:
        if obj is void:
            return
        if self.cached_var is not self._Missing():
            return self.cached_var
        result = self.cached_var = self._func(obj)
        invalidate_method_name = self.build_invalidate_method_name(self._func.__name__)
        setattr(obj, invalidate_method_name, self.invalidate)
        return result

    def invalidate(self) -> void:
        self.cached_var = self._Missing()


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
        result = self._func(cls)
        setattr(cls, self.__name__, result)
        return result
