from version_checking import get_current_version, PythonVersion, _assert_py_version

_assert_py_version(PythonVersion(3, 6))

from decimal import Decimal
from typing import *

void = NULL = null = nil = type(None)

if get_current_version() >= PythonVersion(3, 9):
    list_type = list
    dict_type = dict
    tuple_type = tuple
    set_type = set
else:
    list_type = List
    dict_type = Dict
    tuple_type = Tuple
    set_type = Set

if get_current_version() >= PythonVersion(3, 10):
    Number_t = int | float | complex | Decimal
    string_like = str | bytes
    primitives = int | float | void | string_like | bool
    single_value_iterables = list_type | tuple_type | set_type | frozenset
else:
    Number_t = Union[int, float, complex, Decimal]
    string_like = Union[str, bytes]
    primitives = Union[int, float, void, string_like, bool]
    single_value_iterables = Union[list_type, tuple_type, set_type, frozenset]

Function = Method = Callable
HashMap = dict


def const(t_: type) -> type:
    return Final[t_]


def safe_type(type_: type) -> Union:
    return Union[type_, void]


def is_of_type(actual_t: Any, expected_t: type) -> bool:
    if hasattr(expected_t, '__args__'):
        return actual_t in expected_t.__args__
    return actual_t == expected_t
