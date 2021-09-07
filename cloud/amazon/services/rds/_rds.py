import warnings

from botocore.client import BaseClient

from cloud.amazon.common.aws_service_name_mapping import AWSServiceNameMapping
from cloud.amazon.common.base_service import BaseAmazonService
from cloud.amazon.common.exception_handling import ExceptionLevels
from cloud.amazon.common.service_availability import ServiceAvailability
from types_extensions import void, const, list_type, dict_type


class AmazonRDS(BaseAmazonService):
    # plan: List instances, describe one instance, bring up, enable/disable, destroy, backup/replicate

    def __init__(self, profile: str = None, region: str = None, default_exception_level: int = None) -> void:

        super().__init__(profile, region, default_exception_level)
        self._client: const(BaseClient) = self._backend.client(AWSServiceNameMapping.RDS, region_name=self.region)

    def check_service_availability(self) -> int:
        # Not done, for now assumed RDS is up.
        status = ServiceAvailability.OFFLINE
        if 1 == 1:
            status |= ServiceAvailability.ONLINE
        if 2 == 2:
            status |= ServiceAvailability.CONNECTED
        return status

    @property
    def name(self) -> str:
        return AWSServiceNameMapping.RDS

    def list_db_instances(self, exception_level: int = None) -> list_type[str]:
        if not self._assert_connection(exception_level):
            return []
        try:
            aws_resp = self._client.describe_db_instances()
            return [instance_['DBInstanceIdentifier'] for instance_ in aws_resp['DBInstances']]
        except Exception as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"An unknown exception occurred while trying to list databases:\nThe error is:\n{e}")

    def describe_db_instance(self, instance_name: str, exception_level: int = None) -> dict_type:
        if not self._assert_connection(exception_level):
            return {}
        try:
            aws_resp = self._client.describe_db_instances(
                DBInstanceIdentifier=instance_name
            )
            if instances := aws_resp.get('DBInstances'):
                return instances[0]
        except Exception as e:
            if exception_level == ExceptionLevels.RAISE:
                raise
            if exception_level == ExceptionLevels.WARN:
                warnings.warn(f"An unknown exception occurred while trying to:\n"
                              f"Describe: {instance_name}\nThe error is:\n{e}")
