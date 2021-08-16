import abc

import boto3
from botocore.client import BaseClient

from meta.singleton_meta import SingletonMeta


class BaseAmazonService(metaclass=(SingletonMeta, abc.ABCMeta)):

    _backend: boto3.Session = boto3.Session()
    _client: BaseClient

    @abc.abstractmethod
    def check_service_availability(self) -> int:
        raise NotImplementedError

    @property
    def backend(self) -> boto3.Session:
        return self._backend

    @property
    def client(self) -> BaseClient:
        return self._client
