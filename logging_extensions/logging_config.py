from date_and_time.dt_formatting_styles import DTFormatter
from logging_extensions.severity.log_levels import LogLevels, Severity
from meta.config_meta import BaseConfig
from types_extensions import list_type, const, void


class LoggingConfig(BaseConfig):
    log_level: Severity
    compression_level: int
    handler_classes: list_type[type]
    DT_FORMATTER: const(DTFormatter) = DTFormatter()
    DT_IDENTIFIER: const(str) = '$$datetime'
    SEVERITY_IDENTIFIER: const(str) = '$$severity'
    LOGGER_NAME_IDENTIFIER: const(str) = '$$name'
    MSG_IDENTIFIER: const(str) = '$$msg'
    FIELDS_IDENTIFIER: const(str) = '$$fields'
    string_log_fmt: str = f"[{DT_IDENTIFIER}][{SEVERITY_IDENTIFIER}][{LOGGER_NAME_IDENTIFIER}] " \
                          f"<<{MSG_IDENTIFIER}>> FIELDS: {FIELDS_IDENTIFIER}"

    def __init__(self, log_level: Severity, compression_level: int, handler_classes: list_type[type]) -> void:
        self.log_level: Severity = log_level
        self.compression_level: int = compression_level
        self.handler_classes: list_type[type] = handler_classes

    @classmethod
    def get_config(cls, *, log_level: str = None, compression_level: int = 9,
                   handler_classes: list_type[type] = None, **__) -> 'LoggingConfig':
        return LoggingConfig(
            log_level=log_level or LogLevels.INFO,
            compression_level=compression_level,
            handler_classes=handler_classes or [],
        )
