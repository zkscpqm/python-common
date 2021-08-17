import warnings

from botocore import exceptions as aws_exceptions

from cloud.amazon.common.exception_handling import ExceptionLevels
from types_extensions import const, safe_type

import boto3

from cloud.amazon.aws_service_name_mapping import AWSServiceNameMapping
from cloud.amazon.common.base_service import BaseAmazonService, BaseClient
from cloud.amazon.common.service_availability import ServiceAvailability


class AmazonS3(BaseAmazonService):

    def __init__(self, profile: str = None, region: str = None, default_exception_level: int = None,
                 delimiter: str = '', bucket_prefix: str = '', bucket_suffix: str = ''):
        if profile:
            self._backend: boto3.Session = boto3.Session(profile_name=profile)
        self.default_exception_level: int = default_exception_level or ExceptionLevels.RAISE
        self.delimiter: str = delimiter
        self.prefix: str = bucket_prefix
        self.suffix: str = bucket_suffix
        self.region: str = region or self._backend.region_name
        self._client: const(BaseClient) = self._backend.client(AWSServiceNameMapping.S3, region_name=region)

    @property
    def name(self) -> str:
        return AWSServiceNameMapping.S3

    def build_bucket_name(self, bucket_name: str) -> str:
        if self.prefix:
            bucket_name = f'{self.prefix}{self.delimiter}{bucket_name}'
        if self.suffix:
            bucket_name = f'{bucket_name}{self.delimiter}{self.suffix}'
        return bucket_name

    def check_service_availability(self) -> int:
        status = ServiceAvailability.OFFLINE
        if 1 == 1:
            status |= ServiceAvailability.ONLINE
        if 2 == 2:
            status |= ServiceAvailability.CONNECTED
        return status

    def is_connected(self) -> bool:
        return (self.check_service_availability() & ServiceAvailability.CONNECTED) == ServiceAvailability.CONNECTED

    def get_buckets(self, exception_level: int = None) -> list[str]:
        exception_level = exception_level or self.default_exception_level
        if not self.is_connected():
            if exception_level == ExceptionLevels.RAISE:
                raise aws_exceptions.ConnectionError
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"Could not connect to s3. Please check your connection and try again.")
            return []
        aws_resp = self._client.list_buckets()
        return [bucket_name['Name'] for bucket_name in aws_resp['Buckets']]

    def create_bucket(self, bucket_name: str, apply_format: bool = True,
                      acl: str = 'private', region: str = None, lock_enabled: bool = True,
                      exception_level: int = None) -> safe_type(str):
        exception_level = exception_level or self.default_exception_level
        region = region or self.region
        if apply_format:
            bucket_name = self.build_bucket_name(bucket_name)
        try:
            aws_resp = self._client.create_bucket(
                ACL=acl,
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region},
                ObjectLockEnabledForBucket=lock_enabled
            )
            return aws_resp['Location']

        except (self._client.exceptions.BucketAlreadyExists,
                self._client.exceptions.BucketAlreadyOwnedByYou):
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"A bucket with the same name ({bucket_name}) and permissions already exists.")
            return bucket_name

        except aws_exceptions.ClientError as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                if "InvalidBucketName" in str(e):
                    warnings.warn(f"The given bucket name: {bucket_name} is not valid!  Bucket was not created!")
            return

        except Exception as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            kw_ = "was not created."
            rv = None
            if bucket_name in self.get_buckets():
                kw_ = "was created."
                rv = bucket_name
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"An unknown exception occurred. The bucket {kw_}")
            return rv
