import os
import warnings
from typing import Any

from botocore import exceptions as aws_exceptions

from cloud.amazon.common.aws_util import extract_aws_response_status_code
from cloud.amazon.common.exception_handling import ExceptionLevels, InvalidArgumentException, \
    MissingParametersException
from cloud.amazon.services.s3.exceptions import BucketNotEmptyException
from types_extensions import const, safe_type, void, list_type, dict_type

from cloud.amazon.common.aws_service_name_mapping import AWSServiceNameMapping
from cloud.amazon.common.base_service import BaseAmazonService, BaseClient
from cloud.amazon.common.service_availability import ServiceAvailability
from cloud.amazon.services.s3._storage_class import S3StorageClass
from cloud.amazon.services.s3._bucket import AmazonS3Bucket


class AmazonS3(BaseAmazonService):

    def __init__(self, profile: str = None, region: str = None, default_exception_level: int = None,
                 default_storage_class: str = None, delimiter: str = '', bucket_prefix: str = '',
                 bucket_suffix: str = '') -> void:
        super().__init__(profile, region, default_exception_level)

        self.default_storage_class: str = default_storage_class or S3StorageClass.STANDARD

        self.delimiter: str = delimiter
        self.prefix: str = bucket_prefix
        self.suffix: str = bucket_suffix

        self._client: const(BaseClient) = self._backend.client(AWSServiceNameMapping.S3, region_name=self.region)

    @property
    def name(self) -> str:
        return AWSServiceNameMapping.S3

    def check_service_availability(self) -> int:
        # Not done, for now assumed S3 is up.
        status = ServiceAvailability.OFFLINE
        if 1 == 1:
            status |= ServiceAvailability.ONLINE
        if 2 == 2:
            status |= ServiceAvailability.CONNECTED
        return status

    def list_buckets(self, exception_level: int = None) -> list_type[str]:

        exception_level = exception_level or self.default_exception_level
        if not self._assert_connection(exception_level):
            return []
        try:
            aws_resp = self._client.list_buckets()
            return [bucket_name['Name'] for bucket_name in aws_resp['Buckets']]
        except Exception as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"An unknown exception occurred while trying to list buckets:\nThe error is:\n{e}")

    def list_buckets_as_objects(self, exception_level: int = None) -> list_type[AmazonS3Bucket]:

        exception_level = exception_level or self.default_exception_level
        if not self._assert_connection(exception_level):
            return []
        try:
            aws_resp = self._client.list_buckets()
            return [
                self.spawn_bucket_object(
                    bucket_name=bucket['Name'],
                    apply_format_to_bucket=False,
                    exception_level=exception_level
                )
                for bucket in aws_resp['Buckets']
            ]
        except Exception as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"An unknown exception occurred while trying to list bucket objects:\nThe error is:\n{e}")

    def spawn_bucket_object(self, bucket_name: str, apply_format_to_bucket: bool = True,
                            exception_level: int = None) -> safe_type(AmazonS3Bucket):

        exception_level = exception_level or self.default_exception_level
        ok, region, bucket_name = self._setup(
            exception_level=exception_level,
            root_name=bucket_name,
            build_full_name=apply_format_to_bucket
        )
        if not ok:
            return None

        return AmazonS3Bucket(
            bucket_name=bucket_name,
            parent=self,
            exception_level=exception_level
        )

    def create_bucket(self, bucket_obj: AmazonS3Bucket = None, bucket_name: str = None,
                      apply_format_to_bucket: bool = True, acl: str = 'private',
                      region: str = None, lock_enabled: bool = False, exception_level: int = None,
                      **kwargs) -> safe_type(AmazonS3Bucket):

        exception_level = exception_level or self.default_exception_level
        if not bucket_obj and not bucket_name:
            self._handle_missing_bucket_params(exception_level)
        ok, region, bucket_name = self._setup(
            exception_level=exception_level,
            region=region,
            root_name=bucket_name if not bucket_obj else bucket_obj.bucket_name,
            build_full_name=apply_format_to_bucket if not bucket_obj else False
        )
        if not ok:
            return None

        bucket_obj = bucket_obj or self.spawn_bucket_object(
            bucket_name=bucket_name,
            apply_format_to_bucket=False,
            exception_level=exception_level
        )
        try:
            aws_resp = self._client.create_bucket(
                ACL=acl,
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region},
                ObjectLockEnabledForBucket=lock_enabled,
                **kwargs
            )
            if extract_aws_response_status_code(aws_resp) < 300:
                return bucket_obj

        except (self._client.exceptions.BucketAlreadyExists,
                self._client.exceptions.BucketAlreadyOwnedByYou):
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"A bucket with the same name ({bucket_name}) and permissions already exists.")
            return bucket_obj

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
            if bucket_name in self.list_buckets(exception_level=exception_level):
                kw_ = "was"
                rv = bucket_obj
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"An unknown exception occurred. The bucket {kw_} created. The error is:\n{e}")
            return rv

    def delete_bucket(self, bucket_obj: AmazonS3Bucket = None, bucket_name: str = None,
                      apply_format_to_bucket: bool = True, force_delete_contents: bool = False,
                      exception_level: int = None, **kwargs) -> void:

        exception_level = exception_level or self.default_exception_level
        if not bucket_obj and not bucket_name:
            self._handle_missing_bucket_params(exception_level)
        ok, _, bucket_name = self._setup(
            exception_level=exception_level,
            root_name=bucket_name if not bucket_obj else bucket_obj.bucket_name,
            build_full_name=apply_format_to_bucket if not bucket_obj else False
        )
        if not ok:
            return

        contents = self.get_objects_in_bucket(
            bucket_obj=bucket_obj,
            bucket_name=bucket_name,
            apply_format_to_bucket=False,
            exception_level=exception_level
        )

        if force_delete_contents:
            if contents:
                self.delete_objects_from_bucket(
                    bucket_obj=bucket_obj,
                    bucket_name=bucket_name,
                    object_names=[val for val in contents.values()],
                    permanently=True,
                    apply_format_to_bucket=False,
                    exception_level=exception_level
                )
        else:
            if contents:
                raise BucketNotEmptyException
        try:
            self._client.delete_bucket(Bucket=bucket_name, **kwargs)
        except aws_exceptions.ClientError as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            e = str(e)
            if 'AccessDenied' in e:
                if exception_level == ExceptionLevels.WARN:
                    warnings.warn(f"An access-denied error was encountered while deleting bucket {bucket_name}.\n"
                                  f"You might not have permissions to delete it, or it doesn't exist.\nError:\n{e}")
        except Exception as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                force = " force" if force_delete_contents else ""
                warnings.warn(f"An unknown exception occurred while trying to{force}:\n"
                              f"Delete {bucket_name}\nThe error is:\n{e}")

    def get_objects_in_bucket(self, bucket_obj: AmazonS3Bucket = None, bucket_name: str = None,
                              apply_format_to_bucket: bool = True, exception_level: int = None,
                              mode: str = 'mapping', **kwargs) -> dict:

        _allowed_modes = {'raw', 'mapping'}
        exception_level = exception_level or self.default_exception_level
        if mode not in _allowed_modes:
            raise InvalidArgumentException(mode, _allowed_modes)

        if not bucket_obj and not bucket_name:
            self._handle_missing_bucket_params(exception_level)
        ok, _, bucket_name = self._setup(
            exception_level=exception_level,
            root_name=bucket_name if not bucket_obj else bucket_obj.bucket_name,
            build_full_name=apply_format_to_bucket if not bucket_obj else False
        )
        if not ok:
            return {}

        try:
            if bucket_objects := self._client.list_objects(Bucket=bucket_name, **kwargs).get('Contents'):
                match mode:

                    case x if x == 'raw':
                        return bucket_objects

                    case x if x == 'mapping':
                        return {obj['Key']: obj for obj in bucket_objects}

        except Exception as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"An unknown exception occurred while trying to get object_names:\n"
                              f"From {bucket_name}.\nThe error is:\n{e}")
        return {}

    def put_object_in_bucket(self, object_path: str, bucket_obj: AmazonS3Bucket = None, bucket_name: str = None,
                             apply_format_to_bucket: bool = True, object_name: str = None, exception_level: int = None,
                             storage_class: str = None, acl: str = 'private', encryption: str = 'aws:kms',
                             metadata: dict_type[str, str] = None, **kwargs) -> bool:

        exception_level = exception_level or self.default_exception_level
        storage_class = storage_class or self.default_storage_class
        object_name = object_name or object_path

        if not bucket_obj and not bucket_name:
            self._handle_missing_bucket_params(exception_level)
        ok, _, bucket_name = self._setup(
            exception_level=exception_level,
            root_name=bucket_name if not bucket_obj else bucket_obj.bucket_name,
            build_full_name=apply_format_to_bucket if not bucket_obj else False
        )
        if not ok:
            return False

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
                Key=object_name,
                ExtraArgs={**kwargs, **extra_args}
            )
            return True
        except aws_exceptions.ClientError as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"Client error: {e}!")

        except Exception as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"An unknown exception occurred while:\n"
                              f"Putting local: {object_path}\nAs: {object_name}\nInto: {bucket_name}\n"
                              f"The error is:\n{e}")
        return False

    def get_all_object_versions(self, object_name: str, bucket_obj: AmazonS3Bucket = None, bucket_name: str = None,
                                match_exact: bool = True, apply_format_to_bucket: bool = True,
                                exception_level: int = None, **kwargs) -> list_type[dict_type[str, str]]:

        rv = []

        if not bucket_obj and not bucket_name:
            self._handle_missing_bucket_params(exception_level)

        ok, _, bucket_name = self._setup(
            exception_level=exception_level,
            root_name=bucket_name if not bucket_obj else bucket_obj.bucket_name,
            build_full_name=apply_format_to_bucket if not bucket_obj else False
        )

        if not ok:
            return rv

        try:
            resp = self._client.list_object_versions(
                Bucket=bucket_name,
                Prefix=object_name,
                **kwargs
            )
            for version in resp.get("Versions", []) + resp.get("DeleteMarkers", []):
                key = version.get("Key")
                if match_exact and key != object_name:
                    continue
                rv.append({"Key": key,
                           "VersionId": version.get("VersionId")})
        except Exception as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"An unknown exception occurred while trying to enumerate versions:\n"
                              f"For {object_name}\nIn {bucket_name}.\nThe error is:\n{e}")
        return rv

    def delete_object_from_bucket(self, object_name: str, bucket_obj: AmazonS3Bucket = None, bucket_name: str = None,
                                  permanently: bool = False, apply_format_to_bucket: bool = True,
                                  exception_level: int = None, **kwargs) -> void:

        exception_level = exception_level or self.default_exception_level

        if not bucket_obj and not bucket_name:
            self._handle_missing_bucket_params(exception_level)

        ok, _, bucket_name = self._setup(
            exception_level=exception_level,
            root_name=bucket_name if not bucket_obj else bucket_obj.bucket_name,
            build_full_name=apply_format_to_bucket if not bucket_obj else False
        )

        if not ok:
            return

        try:
            if permanently:
                all_versions = self.get_all_object_versions(
                    object_name=object_name,
                    bucket_obj=bucket_obj,
                    bucket_name=bucket_name,
                    apply_format_to_bucket=False,
                    exception_level=exception_level,
                    **kwargs
                )
                if len(all_versions) > 0:
                    self._client.delete_objects(
                        Bucket=bucket_name,
                        Delete={
                            'Objects': all_versions,
                            'Quiet': True
                        },
                        **kwargs
                    )
            else:
                self._client.delete_object(
                    Bucket=bucket_name,
                    Key=object_name,
                    **kwargs
                )
        except Exception as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                permanently = " permanently" if permanently else ""
                warnings.warn(f"An unknown exception occurred while trying to{permanently}:\n"
                              f"Delete {object_name}\nFrom {bucket_name}.\nThe error is:\n{e}")

    def delete_objects_from_bucket(self, object_names: list_type[str], bucket_obj: AmazonS3Bucket = None,
                                   bucket_name: str = None, permanently: bool = False,
                                   apply_format_to_bucket: bool = True,
                                   exception_level: int = None, **kwargs) -> void:

        exception_level = exception_level or self.default_exception_level

        if not bucket_obj and not bucket_name:
            self._handle_missing_bucket_params(exception_level)

        ok, _, bucket_name = self._setup(
            exception_level=exception_level,
            root_name=bucket_name if not bucket_obj else bucket_obj.bucket_name,
            build_full_name=apply_format_to_bucket if not bucket_obj else False
        )

        if not ok:
            return

        try:
            objects_to_delete = []
            for object_name in object_names:
                if permanently:
                    all_versions = self.get_all_object_versions(
                        bucket_obj=bucket_obj,
                        bucket_name=bucket_name,
                        object_name=object_name,
                        apply_format_to_bucket=False,
                        exception_level=exception_level,
                        **kwargs
                    )
                    objects_to_delete.extend(all_versions)
                else:
                    objects_to_delete.append({"Key": object_name})
            if len(objects_to_delete) > 0:
                self._client.delete_objects(
                    Bucket=bucket_name,
                    Delete={
                        'Objects': objects_to_delete,
                        'Quiet': True
                    },
                    **kwargs
                )
        except Exception as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                permanently = " permanently" if permanently else ""
                warnings.warn(f"An unknown exception occurred while trying to{permanently} bulk:\n"
                              f"Delete {object_names}\nFrom {bucket_name}.\nThe error is:\n{e}")

    def download_object_from_bucket(self, object_name: str, destination: str, bucket_obj: AmazonS3Bucket = None,
                                    bucket_name: str = None, apply_format_to_bucket: bool = True,
                                    exception_level: int = None, **kwargs) -> void:

        if not bucket_obj and not bucket_name:
            self._handle_missing_bucket_params(exception_level)

        ok, _, bucket_name = self._setup(
            exception_level=exception_level,
            root_name=bucket_name if not bucket_obj else bucket_obj.bucket_name,
            build_full_name=apply_format_to_bucket if not bucket_obj else False
        )

        if not ok:
            return

        path_to, _ = os.path.split(destination)
        if not os.path.isdir(path_to):
            os.makedirs(path_to, exist_ok=True)
        buffer = open(destination, 'wb')

        try:
            self._client.download_fileobj(
                Bucket=bucket_name,
                Key=object_name,
                Fileobj=buffer,
                **kwargs
            )

        except Exception as e:
            if exception_level == ExceptionLevels.RAISE:
                if buffer:
                    buffer.close()
                raise
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"An unknown exception occurred while trying to:\n"
                              f"Download {object_name}\nFrom {bucket_name}\nTo {destination}\nThe error is:\n{e}")
        finally:
            if buffer:
                buffer.close()

    def _handle_missing_bucket_params(self, exception_level: int = None, default_return_value: Any = None):

        exception_level = exception_level or self.default_exception_level
        err_msg = f"You need to provide either an AmazonS3Bucket object or a bucket name"
        if exception_level == ExceptionLevels.RAISE:
            raise MissingParametersException(msg=err_msg, parameter_names=['bucket_obj', 'bucket_name'])
        if exception_level == ExceptionLevels.WARN:
            warnings.warn(err_msg)
        return default_return_value
