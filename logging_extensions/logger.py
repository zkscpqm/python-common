from typing import Any
from datetime import datetime as _dt

from logging_extensions.handlers.text_file_write_handler import TextFileWriteHandler
from logging_extensions.severity.log_levels import LogLevels
from logging_extensions.log_message import LogMessage
from logging_extensions.logging_config import LoggingConfig
from logging_extensions.severity.severity import Severity
from types_extensions import void, const, dict_type, list_type
from logging_extensions.handlers.base_log_handler import BaseLogHandler


# zipped_b = gzip.compress(bytes("string", 'utf-8'), compresslevel=9)


class LoggerPlus:

    _DEFAULT_HANDLERS: list_type[BaseLogHandler] = [TextFileWriteHandler]

    def __init__(self, name: str = None, config: LoggingConfig = None, enabled: bool = True,
                 include_default_handlers: bool = True, **config_kwargs) -> void:
        self._initialized: bool = False
        self.name: const(str) = name or 'Unnamed'
        self.enabled: bool = enabled
        self.config: LoggingConfig = config or LoggingConfig.get_config(**config_kwargs)
        self.handlers: list[BaseLogHandler] = []
        self._init(include_default_handlers, **config_kwargs)

    def _init(self, include_default_handlers: bool, **kwargs) -> void:
        kwargs = kwargs or {}
        handler_classes = self.config.handler_classes
        if include_default_handlers:
            handler_classes += self._DEFAULT_HANDLERS
        for handler_class in self.config.handler_classes:
            handler = handler_class(
                logger_name=self.name,
                parent_config=self.config,
                enabled=self.enabled,
                **kwargs
            )
            self.handlers.append(handler)
        self._initialized = True

    def _log(self, severity: Severity, message: str = '', fields: dict_type[str, Any] = None,
             message_format_mapping: dict_type[str, Any] = None, **handler_kwargs) -> void:
        message_ = LogMessage(message=message,
                              timestamp=_dt.now(),
                              severity=severity,
                              fields=fields,
                              message_format_mapping=message_format_mapping)
        for handler in self.handlers:
            handler.handle_message(message=message_, **handler_kwargs)

    def debug(self, message: str = '', fields: dict_type[str, Any] = None,
              message_format_mapping: dict_type[str, Any] = None, **handler_kwargs):
        self._log(
            LogLevels.DEBUG,
            message,
            fields,
            message_format_mapping,
            **handler_kwargs
        )

    def info(self, message: str = '', fields: dict_type[str, Any] = None,
             message_format_mapping: dict_type[str, Any] = None, **handler_kwargs):
        self._log(
            LogLevels.INFO,
            message,
            fields,
            message_format_mapping,
            **handler_kwargs
        )

    def warning(self, message: str = '', fields: dict_type[str, Any] = None,
                message_format_mapping: dict_type[str, Any] = None, **handler_kwargs):
        self._log(
            LogLevels.WARNING,
            message,
            fields,
            message_format_mapping,
            **handler_kwargs
        )

    def error(self, message: str = '', fields: dict_type[str, Any] = None,
              message_format_mapping: dict_type[str, Any] = None, **handler_kwargs):
        self._log(
            LogLevels.ERROR,
            message,
            fields,
            message_format_mapping,
            **handler_kwargs
        )

    def enable(self) -> void:
        self.enabled = True
        for handler in self.handlers:
            handler.enabled = True

    def disable(self) -> void:
        self.enabled = False
        for handler in self.handlers:
            handler.enabled = False
