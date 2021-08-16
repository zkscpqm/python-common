from types_extensions import const

import boto3

from cloud.amazon.aws_service_name_mapping import AWSServiceNameMapping
from cloud.amazon.common.base_service import BaseAmazonService, BaseClient
from cloud.amazon.common.service_availability import ServiceAvailability


class AmazonS3(BaseAmazonService):

    def __init__(self, profile: str = None, region: str = None):
        if profile:
            self._backend: boto3.Session = boto3.Session(profile_name=profile)
        self._client: const(BaseClient) = self._backend.client(AWSServiceNameMapping.S3, region_name=region)

    def check_service_availability(self) -> int:
        status = ServiceAvailability.OFFLINE
        if 1 == 1:
            status |= ServiceAvailability.ONLINE
        if 2 == 2:
            status |= ServiceAvailability.CONNECTED
        return status

    def get_buckets(self) -> list[str]:
        return
