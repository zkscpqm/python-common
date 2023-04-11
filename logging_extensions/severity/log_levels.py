from logging_extensions.severity.mapping import SeverityLabelMapping, SeverityLevelMapping
from logging_extensions.severity.severity import Severity
from meta.config_meta import FinalConfigMeta
from types_extensions import const


class LogLevels(metaclass=FinalConfigMeta):

    DEBUG: const(Severity) = Severity(text=SeverityLabelMapping.DEBUG, level=SeverityLevelMapping.DEBUG)
    INFO: const(Severity) = Severity(text=SeverityLabelMapping.INFO, level=SeverityLevelMapping.INFO)
    WARNING: const(Severity) = Severity(text=SeverityLabelMapping.WARNING, level=SeverityLevelMapping.WARNING)
    ERROR: const(Severity) = Severity(text=SeverityLabelMapping.ERROR, level=SeverityLevelMapping.ERROR)
