from decimal import Decimal
from typing import *


Number_t = int | float | Decimal
Function = Method = Callable
void = NULL = null = None
string = str
string_like = str | bytes


def safe_type(type_: type) -> Union:
    return type_ | void
