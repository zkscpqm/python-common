import re
from typing import Any
from types_extensions import tuple_type


def split_string(str_: str, index: int) -> tuple_type[str, str]:
    """
    Takes a string and returns a tuple of the string, split at the index given
    """
    if index >= len(str_):
        raise IndexError
    return str_[:index], str_[index:]


def multiple_replace(input_string: str, kwargs_dict: dict[str: Any]):
    """
    Replaces each occurring key (from kwargs_dict) with its value in input_string.
    Useful in cases where f-strings or {} formatting can't be used
    """
    pattern = re.compile("|".join([re.escape(key) for key in kwargs_dict.keys()]))
    return pattern.sub(lambda x: str(kwargs_dict[x.group(0)]), input_string)
