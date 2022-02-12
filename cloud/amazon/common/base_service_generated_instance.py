import abc

from types_extensions import void


class BaseSGI(metaclass=abc.ABCMeta):

    def __init__(self, *, parent, exception_level: int) -> void:
        self.exception_level: int = exception_level
        self.parent = parent

    @classmethod
    @abc.abstractmethod
    def from_aws_response(cls, aws_resp: dict, parent, exception_level: int, **kwargs) -> 'BaseSGI':
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, *args, **kwargs) -> 'BaseSGI':
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *args, **kwargs) -> void:
        raise NotImplementedError
