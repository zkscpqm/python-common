import dataclasses
from datetime import datetime as _dt
from typing import Any

from logging_extensions.severity.log_levels import LogLevels, Severity
from types_extensions import const, dict_type, void, list_type


@dataclasses.dataclass(init=False)
class LogMessage:

    severity: const(Severity)
    timestamp: const(_dt)
    message: str
    fields: dict_type[str, Any]

    def __init__(self, message: str, timestamp: _dt, severity: Severity = LogLevels.INFO,
                 fields: dict_type[str, Any] = None, message_format_mapping: dict_type[str, Any] = None):
        self.timestamp: const(_dt) = timestamp
        self.severity: const(Severity) = severity
        self.fields: dict_type[str, Any] = fields
        message_format_mapping = message_format_mapping or {}
        self.message = message.format(**message_format_mapping)

    def register_field(self, location: list_type[str], value: Any) -> void:
        path = {}
        curr = path
        for i, loc_ in enumerate(location):
            if i == len(location) - 1:
                curr[loc_] = value
            else:
                curr[loc_] = {}
                curr = curr[loc_]

        self.fields.update()

    def register_fields(self, fields: dict[str: Any]) -> void:
        self.fields.update(fields)
