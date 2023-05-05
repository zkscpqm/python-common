from typing import Any

from cloud.amazon.common.base_service_generated_instance import BaseSGI
from properties_and_methods import CachedProperty
from types_extensions import void, const, list_type, dict_type


class AmazonRDSInstance(BaseSGI):

    def __init__(self, db_name: str, db_instance_identifier: str, db_instance_class: str, db_engine: str,
                 db_port: int, parent, exception_level: int) -> void:
        super().__init__(parent=parent, exception_level=exception_level)
        self.db_name: const(str) = db_name
        self.db_instance_identifier: const(str) = db_instance_identifier
        self.db_instance_class: const(str) = db_instance_class
        self.db_engine: const(str) = db_engine
        self.db_port: const(int) = db_port

    def set_exception_level(self, new_level: int) -> void:
        self.exception_level = new_level
        self.invalidate_cached_property_defaults()

    @classmethod
    def from_aws_response(cls, aws_resp: dict, parent, exception_level: int, **kwargs) -> 'AmazonRDSInstance':
        ...

    @CachedProperty
    def defaults(self):
        return dict(
            rds_obj=self,
            exception_level=self.exception_level,
        )

    def _build_default_params(self, **kwargs) -> dict_type[str, Any]:
        return {**self.defaults, **kwargs}

    def create(self, acl: str = 'private', region: str = None, **kwargs) -> 'AmazonRDSInstance':
        ...

    def delete(self, force_delete_contents: bool = False, **kwargs) -> void:
        ...
