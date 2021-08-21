import boto3
from botocore.client import BaseClient

from cloud.amazon.common.aws_service_name_mapping import AWSServiceNameMapping
from cloud.amazon.common.base_service import BaseAmazonService
from cloud.amazon.common.exception_handling import ExceptionLevels
from cloud.amazon.common.service_availability import ServiceAvailability
from types_extensions import void, const


class AmazonEC2(BaseAmazonService):

    def __init__(self, profile: str = None, region: str = None, default_exception_level: int = None,
                 delimiter: str = '', instance_name_prefix: str = '', instance_name_suffix: str = '') -> void:
        if profile:
            self._backend: boto3.Session = boto3.Session(profile_name=profile)
        self.prefix: str = instance_name_prefix
        self.suffix: str = instance_name_suffix
        self.delimiter: str = delimiter
        self.default_exception_level: int = default_exception_level or ExceptionLevels.RAISE
        self.region: str = region or self._backend.region_name
        self._client: const(BaseClient) = self._backend.client(AWSServiceNameMapping.EC2, region_name=region)

    def check_service_availability(self) -> int:
        # Not done, for now assumed EC2 is up.
        status = ServiceAvailability.OFFLINE
        if 1 == 1:
            status |= ServiceAvailability.ONLINE
        if 2 == 2:
            status |= ServiceAvailability.CONNECTED
        return status

    @property
    def name(self) -> str:
        return AWSServiceNameMapping.EC2

    def build_instance_name(self, instance_name: str) -> str:
        if self.prefix:
            instance_name = f'{self.prefix}{self.delimiter}{instance_name}'
        if self.suffix:
            instance_name = f'{instance_name}{self.delimiter}{self.suffix}'
        return instance_name
