import warnings

import botocore.exceptions
from botocore import exceptions as aws_exceptions

from cloud.amazon.common.exception_handling import ExceptionLevels, InvalidArgumentException
from meta.config_meta import FinalConfigMeta
from types_extensions import const, safe_type, void, list_type, dict_type

import boto3

from cloud.amazon.common.aws_service_name_mapping import AWSServiceNameMapping
from cloud.amazon.common.base_service import BaseAmazonService, BaseClient
from cloud.amazon.common.service_availability import ServiceAvailability


class AmazonS3(BaseAmazonService):

    def __init__(self, profile: str = None, region: str = None, default_exception_level: int = None,
                 default_storage_class: str = None, delimiter: str = '', bucket_prefix: str = '',
                 bucket_suffix: str = '') -> void:
        if profile:
            self._backend: boto3.Session = boto3.Session(profile_name=profile)
        self.default_storage_class: str = default_storage_class or S3StorageClass.STANDARD

        if default_exception_level:
            self.default_exception_level = default_exception_level
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
        # Not done, for now assumed S3 is up.
        status = ServiceAvailability.OFFLINE
        if 1 == 1:
            status |= ServiceAvailability.ONLINE
        if 2 == 2:
            status |= ServiceAvailability.CONNECTED
        return status

    def get_buckets(self, exception_level: int = None) -> list_type[str]:
        if not self._assert_connection(exception_level):
            return []
        aws_resp = self._client.list_buckets()
        return [bucket_name['Name'] for bucket_name in aws_resp['Buckets']]

    def create_bucket(self, bucket_name: str, apply_format_to_bucket: bool = True,
                      acl: str = 'private', region: str = None, lock_enabled: bool = False,
                      exception_level: int = None, **kwargs) -> safe_type(str):
        exception_level = exception_level or self.default_exception_level
        if not self._assert_connection(exception_level):
            return None
        region = region or self.region
        if apply_format_to_bucket:
            bucket_name = self.build_bucket_name(bucket_name)
        try:
            aws_resp = self._client.create_bucket(
                ACL=acl,
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region},
                ObjectLockEnabledForBucket=lock_enabled,
                **kwargs
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
            kw_ = "was not"
            rv = None
            if bucket_name in self.get_buckets(exception_level=exception_level):
                kw_ = "was"
                rv = bucket_name
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"An unknown exception occurred. The bucket {kw_} created. The error is:\n{e}")
            return rv

    def delete_bucket(self, bucket_name: str, apply_format_to_bucket: bool = True, force_delete_contents: bool = False,
                      exception_level: int = None, **kwargs) -> void:
        exception_level = exception_level or self.default_exception_level
        if not self._assert_connection(exception_level):
            return None
        if apply_format_to_bucket:
            bucket_name = self.build_bucket_name(bucket_name)
        if force_delete_contents:
            contents = self.get_objects_in_bucket(bucket_name,
                                                  apply_format_to_bucket=False,
                                                  exception_level=exception_level
                                                  )
            if contents:
                self.delete_objects_from_bucket(bucket_name,
                                                objects=[val for val in contents.values()],
                                                full_delete=True,
                                                apply_format_to_bucket=False,
                                                exception_level=exception_level)
        try:
            self._client.delete_bucket(Bucket=bucket_name, **kwargs)
        except botocore.exceptions.ClientError as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            e = str(e)
            if 'AccessDenied' in e:
                if exception_level == ExceptionLevels.WARN:
                    warnings.warn(f"An access-denied error was encountered while deleting bucket {bucket_name}.\n"
                                  f"You might not have permissions to delete it, or it doesn't exist.\nError:\n{e}")

    def get_objects_in_bucket(self, bucket_name: str, apply_format_to_bucket: bool = True,
                              exception_level: int = None, mode: str = 'mapping') -> dict:
        _allowed_modes = {'raw', 'mapping'}
        exception_level = exception_level or self.default_exception_level
        if mode not in _allowed_modes:
            raise InvalidArgumentException(mode, _allowed_modes)
        if not self._assert_connection(exception_level):
            return {}
        if apply_format_to_bucket:
            bucket_name = self.build_bucket_name(bucket_name)
        bucket_objects = self._client.list_objects(Bucket=bucket_name)['Contents']
        match mode:

            case x if x == 'raw':
                return bucket_objects

            case x if x == 'mapping':
                return {obj['Key']: obj for obj in bucket_objects}

    def put_object_in_bucket(self, bucket_name: str, object_path: str, apply_format_to_bucket: bool = True,
                             object_name: str = None, exception_level: int = None, storage_class: str = None,
                             acl: str = 'private', encryption: str = 'aws:kms', metadata: dict_type[str, str] = None,
                             **kwargs) -> bool:
        exception_level = exception_level or self.default_exception_level
        storage_class = storage_class or self.default_storage_class
        if not self._assert_connection(exception_level):
            return False
        if apply_format_to_bucket:
            bucket_name = self.build_bucket_name(bucket_name)
        try:
            extra_args = {
                'ACL': acl,
                'StorageClass': storage_class,
                'ServerSideEncryption': encryption,
                'Metadata': metadata or {}
            }
            self._client.upload_file(
                Filename=object_path,
                Bucket=bucket_name,
                Key=object_name or object_path,
                ExtraArgs={**kwargs, **extra_args}
            )
            return True
        except aws_exceptions.ClientError as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"Clienterror: {e}!")

        except Exception as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"An unknown exception occurred. The error is:\n{e}")
        return False

    def delete_object_from_bucket(self, bucket_name: str, object_name: str, full_delete: bool = False,
                                  apply_format_to_bucket: bool = True, exception_level: int = None) -> void:
        exception_level = exception_level or self.default_exception_level
        if not self._assert_connection(exception_level):
            return False
        if apply_format_to_bucket:
            bucket_name = self.build_bucket_name(bucket_name)

    def delete_objects_from_bucket(self, bucket_name: str, objects: list_type[dict_type[str, str]],
                                   full_delete: bool = False, apply_format_to_bucket: bool = True,
                                   exception_level: int = None) -> void:
        exception_level = exception_level or self.default_exception_level
        if not self._assert_connection(exception_level):
            return False
        if apply_format_to_bucket:
            bucket_name = self.build_bucket_name(bucket_name)
        

class S3StorageClass(metaclass=FinalConfigMeta):
    STANDARD: const(str) = 'STANDARD'
    REDUCED_REDUNDANCY: const(str) = 'REDUCED_REDUNDANCY'
    STANDARD_IA: const(str) = 'STANDARD_IA'
    ONEZONE_IA: const(str) = 'ONEZONE_IA'
    INTELLIGENT_TIERING: const(str) = 'INTELLIGENT_TIERING'
    GLACIER: const(str) = 'GLACIER'
    DEEP_ARCHIVE: const(str) = 'DEEP_ARCHIVE'
    OUTPOSTS: const(str) = 'OUTPOSTS'
