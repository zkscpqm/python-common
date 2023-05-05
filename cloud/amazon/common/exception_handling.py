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


class MissingParametersException(Exception):

    def __init__(self, msg: str = None, parameter_names: list_type[str] = None) -> void:
        self.msg = msg or 'Some parameters were missing.'
        self.parameter_names = parameter_names or ['not given']

    def __str__(self) -> str:
        msg = f"{self.msg}\nMissing params: {', '.join(self.parameter_names)}"
        return msg


class InvalidAWSResponseException(Exception):

    def __init__(self, expected_dict_structures: list_type[list_type[str]]) -> void:
        self.expected_dict_structures: list_type[str] = [
            f"aws_response[{']['.join([path_ for path_ in structure])}]"
            for structure in expected_dict_structures
        ]

    def __str__(self) -> str:
        newl_ = "\n"
        msg = f"The AWS Response you provided is invalid. The given dict requires the following paths:\n" \
              f"{newl_.join(self.expected_dict_structures)}"
        return msg
