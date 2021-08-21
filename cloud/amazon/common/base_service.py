import abc
import warnings

import boto3
from botocore.client import BaseClient
from botocore import exceptions as aws_exceptions

from cloud.amazon.common.exception_handling import ExceptionLevels
from cloud.amazon.common.service_availability import ServiceAvailability


class BaseAmazonService(abc.ABC):

    _backend:  boto3.Session = boto3.Session()
    _client: BaseClient
    default_exception_level: int = ExceptionLevels.RAISE

    @abc.abstractmethod
    def check_service_availability(self) -> int:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    def backend(self) -> boto3.Session:
        return self._backend

    @property
    def client(self) -> BaseClient:
        return self._client

    def is_connected(self) -> bool:
        return (self.check_service_availability() & ServiceAvailability.CONNECTED) == ServiceAvailability.CONNECTED

    def _assert_connection(self, exception_level: int = None) -> bool:
        exception_level = exception_level or self.default_exception_level
        if not self.is_connected():
            if exception_level == ExceptionLevels.RAISE:
                raise aws_exceptions.ConnectionError
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"Could not connect to {self.name}. Please check your connection and try again.")
            return False
        return True
