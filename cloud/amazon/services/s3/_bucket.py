from typing import Any

from cloud.amazon.common.base_service_generated_instance import BaseSGI
from properties_and_methods import CachedProperty
from types_extensions import void, const, list_type, dict_type


class AmazonS3Bucket(BaseSGI):

    def __init__(self, bucket_name: str, parent, exception_level: int) -> void:
        super().__init__(exception_level=exception_level)
        self.bucket_name: const(str) = bucket_name
        self.parent = parent

    def set_exception_level(self, new_level: int) -> void:
        self.exception_level = new_level
        self.invalidate_cached_property_defaults()

    @CachedProperty
    def defaults(self):
        return dict(
            bucket_name=self.bucket_name,
            apply_format_to_bucket=False,
            exception_level=self.exception_level,
        )

    def _build_default_params(self, kwargs_dict: dict_type[str, Any]) -> dict_type[str, Any]:
        return {**kwargs_dict, **self.defaults}

    def get_objects(self, mode: str = 'mapping', **kwargs) -> dict:
        return self.parent.get_objects_in_bucket(
            **self._build_default_params(kwargs),
            mode=mode,
        )

    def put_object(self, object_path: str, **kwargs) -> bool:
        return self.parent.put_object_in_bucket(
            **self._build_default_params(kwargs),
            object_path=object_path,
        )

    def delete_object(self, object_name: str, **kwargs) -> void:
        return self.parent.delete_object_from_bucket(
            **self._build_default_params(kwargs),
            object_name=object_name,
        )

    def delete_objects(self, object_names: list_type[str], **kwargs) -> void:
        return self.parent.delete_objects_from_bucket(
            **self._build_default_params(kwargs),
            object_names=object_names,
        )

    def get_all_object_versions(self, object_name: str, **kwargs) -> list_type[dict_type[str, str]]:
        return self.parent.get_all_object_versions(
            **self._build_default_params(kwargs),
            object_name=object_name
        )

    def download_object(self, object_name: str, destination: str, **kwargs) -> void:
        return self.parent.download_object_from_bucket(
            **self._build_default_params(kwargs),
            object_name=object_name,
            destination=destination
        )
