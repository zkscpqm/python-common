import abc

from logging_extensions.log_message import LogMessage
from logging_extensions.logging_config import LoggingConfig
from types_extensions import void, const, safe_type


class BaseLogHandler(metaclass=abc.ABCMeta):

    def __init__(self, logger_name: str, parent_config: LoggingConfig, enabled: bool) -> void:
        self.logger_name: const(str) = logger_name
        self.config: LoggingConfig = parent_config
        self.enabled: bool = enabled
        self.current_log: safe_type(LogMessage) = None

    @abc.abstractmethod
    def handle_message(self, message: LogMessage, **kwargs) -> void:
        raise NotImplementedError

    @abc.abstractmethod
    def flush(self) -> void:
        raise NotImplementedError

    @abc.abstractmethod
    def enable(self) -> void:
        raise NotImplementedError

    @abc.abstractmethod
    def disable(self) -> void:
        raise NotImplementedError

    def _format_time_date_current(self):
        return self.current_log.timestamp.strftime(self.config.DT_FORMATTER.default_time_first())
