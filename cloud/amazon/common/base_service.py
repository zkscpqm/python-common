from version_checking import _assert_py_version, PythonVersion

_assert_py_version(PythonVersion(3, 10))

import abc
import warnings

import boto3
from botocore.client import BaseClient
from botocore import exceptions as aws_exceptions

from cloud.amazon.common.exception_handling import ExceptionLevels
from cloud.amazon.common.service_availability import ServiceAvailability
from types_extensions import tuple_type


class BaseAmazonService(abc.ABC):

    _backend: boto3.Session = boto3.Session()
    _client: BaseClient
    default_exception_level: int = ExceptionLevels.RAISE
    region: str = _backend.region_name

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

    @property
    def is_named(self) -> bool:
        return (
            hasattr(self, 'prefix') and
            hasattr(self, 'delimiter') and
            hasattr(self, 'suffix')
        )

    def is_connected(self) -> bool:
        return (self.check_service_availability() & ServiceAvailability.CONNECTED) == ServiceAvailability.CONNECTED

    def _assert_connection(self, exception_level: int) -> bool:
        exception_level = exception_level or self.default_exception_level
        if not self.is_connected():
            if exception_level == ExceptionLevels.RAISE:
                raise aws_exceptions.ConnectionError
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"Could not connect to {self.name}. Please check your connection and try again.")
            return False
        return True

    def build_full_name(self, root_name: str) -> str:
        if self.is_named and root_name:
            if self.prefix:
                root_name = f'{self.prefix}{self.delimiter}{root_name}'
            if self.suffix:
                root_name = f'{root_name}{self.delimiter}{self.suffix}'
        return root_name

    def _setup(self, *, exception_level: int, region: str = None, root_name: str = None,
               build_full_name: bool = False) -> tuple_type[bool, str, str]:
        name = root_name if not build_full_name else self.build_full_name(root_name)
        region = region or self.region
        if not self._assert_connection(exception_level=exception_level):
            return False, region, name
        return True, region, name

