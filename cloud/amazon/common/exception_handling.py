from typing import Any, Iterable

from types_extensions import const, void, list_type, tuple_type


class ExceptionLevels:

    RAISE: const(int) = 1
    WARN: const(int) = 2
    SILENT: const(int) = 3


class InvalidArgumentException(Exception):

    def __init__(self, given_argument: Any, allowed_arguments: Iterable[Any]) -> void:
        self.given_argument = given_argument
        self.given_argument_type = type(given_argument)
        self.allowed_arguments: list_type[tuple_type[Any, type]] = [(x, type(x)) for x in allowed_arguments]

    def __str__(self) -> str:
        msg = f"Invalid argument ({self.given_argument}) of type ({self.given_argument_type}) given." \
              f"The allowed arguments are {', '.join((f'({x}) of type ({y})' for x, y in self.allowed_arguments))}"
        return msg
