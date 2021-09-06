import abc

from types_extensions import void


class BaseSGI(metaclass=abc.ABCMeta):

    def __init__(self, *, exception_level: int) -> void:
        self.exception_level: int = exception_level
