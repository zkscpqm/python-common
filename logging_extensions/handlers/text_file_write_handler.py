import json
from typing import Any

from logging_extensions.handlers.base_log_handler import BaseLogHandler
from logging_extensions.log_message import LogMessage
from logging_extensions.logging_config import LoggingConfig
from macros.string_macros import multiple_replace
from types_extensions import void, dict_type


class TextFileWriteHandler(BaseLogHandler):

    def __init__(self, logger_name: str, parent_config: LoggingConfig, enabled: bool,
                 text_log_file_location: str, **_) -> void:
        super().__init__(logger_name, parent_config, enabled)
        self.destination: str = text_log_file_location  # TODO: When safe pathing is merged, create safe path
        self.text_buffer: str = ''

    def handle_message(self, message: LogMessage, **kwargs) -> void:
        if self.enabled and message.severity >= self.config.log_level:
            self.current_log = message
            self.text_buffer = self._format_current_as_string()
        self.flush()

    def flush(self) -> void:
        if self.enabled:
            self._flush()
            self.text_buffer = ''
            self.current_log = None

    def _flush(self):
        with open(self.destination, mode='a+') as log_file_h:
            log_file_h.write(self.text_buffer)

    def _format_current_as_string(self) -> str:
        return multiple_replace(
            self.config.string_log_fmt,
            self._build_message_format_kwargs()
        ) + "\n"

    def _build_message_format_kwargs(self) -> dict_type[str: Any]:
        return {
            self.config.DT_IDENTIFIER: self._format_time_date_current(),
            self.config.SEVERITY_IDENTIFIER: self.current_log.severity,
            self.config.LOGGER_NAME_IDENTIFIER: self.logger_name,
            self.config.MSG_IDENTIFIER: self.current_log.message,
            self.config.FIELDS_IDENTIFIER: json.dumps(self.current_log.fields)
        }

    def enable(self) -> void:
        self.enabled = True

    def disable(self) -> void:
        self.enabled = False
