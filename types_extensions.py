from decimal import Decimal
from typing import *


Number_t = int | float | complex | Decimal
Function = Method = Callable
void = NULL = null = nil = type(None)
string_like = str | bytes
HashMap = dict


def const(t_: type) -> type:
    return Final[t_]


def safe_type(type_: type) -> Union:
    return type_ | void
