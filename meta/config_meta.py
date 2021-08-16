from typing import Any
import os
import abc

from types_extensions import void

try:
    import boto3
    boto3_exists: bool = True
except ImportError:
    boto3 = None
    boto3_exists = False


class BasicConfigMeta(type):

    def __getattr__(self, key: str) -> Any:

        for key_instance in (key, key.casefold(), key.upper(), key.capitalize()):
            value = os.environ.get(key_instance)
            if not value:
                value = locals().get(key_instance)
            if not value:
                if boto3_exists:
                    sm = boto3.client("secretsmanager")
                    try:
                        value = sm.get_secret_value(SecretId=key_instance).get("SecretString")
                    except sm.exceptions.ResourceNotFoundException:
                        ...
            if value:
                return value


class BaseConfig(metaclass=(BasicConfigMeta, abc.ABCMeta)):
    ...


class FinalConfigMeta(BasicConfigMeta):

    def __setattr__(self, key: str, value: Any) -> void:
        raise AttributeError("You cannot update the configuration")
