from meta.config_meta import FinalConfigMeta
from types_extensions import const


class SeverityLabelMapping(FinalConfigMeta):
    DEBUG: const(str) = "DEBUG"
    INFO: const(str) = "INFO"
    WARNING: const(str) = "WARNING"
    ERROR: const(str) = "ERROR"


class SeverityLevelMapping(FinalConfigMeta):
    DEBUG: const(int) = 0
    INFO: const(int) = 10
    WARNING: const(int) = 70
    ERROR: const(int) = 95
