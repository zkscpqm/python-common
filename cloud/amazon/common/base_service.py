import abc

import boto3
from botocore.client import BaseClient


class BaseAmazonService(abc.ABC):

    _backend:  boto3.Session = boto3.Session()
    _client: BaseClient

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
