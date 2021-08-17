from typing import Any
import os

from types_extensions import void

try:
    import boto3
    boto3_exists: bool = True
except ImportError:
    boto3 = None
    boto3_exists = False


class BasicConfigMeta(type):
    """
    A configuration metaclass to be set on Config classes which can use either class properties or object properties.
    When attempting to get a non-existent property from a class or instance which implements this as a metaclass,
    the multiple checks will be made in 4 rounds:

    Rounds:
        - The given key as it is
        - The given key forced lowercase
        - The given key forced uppercase
        - The given key forced capitalized

    Checks:
        - The class __dict__
        - Envoronment variables
        - Thread-local storage
        - AWS SecretsManager, assuming boto3 is installed and an AWS account is configured
    """

    def __getattr__(self, key: str) -> Any:

        for key_instance in (key, key.casefold(), key.upper(), key.capitalize()):
            if hasattr(self, '__dict__'):
                value = self.__dict__.get(key)
                if value:
                    return value
            value = os.environ.get(key_instance)
            if not value:
                value = locals().get(key_instance)
            if not value:
                if boto3_exists:
                    sm = boto3.client("secretsmanager")
                    try:
                        value = sm.get_secret_value(SecretId=key_instance).get("SecretString")
                    except:
                        ...
            if value:
                return value


class BaseConfig(metaclass=BasicConfigMeta):
    ...


class FinalConfigMeta(BasicConfigMeta):
    """
    See parent class for basic idea.

    This metaclass will also raise attribute errors if an attempt is made to change any of the initial config values
    """

    def __setattr__(self, key: str, value: Any) -> void:
        raise AttributeError("You cannot update the configuration")
