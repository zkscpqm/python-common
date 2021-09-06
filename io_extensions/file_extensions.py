from meta.config_meta import FinalConfigMeta
from types_extensions import const


class FileExtensions(metaclass=FinalConfigMeta):

    JSON: const(str) = 'json'
    XML: const(str) = 'xml'
    YAML: const(str) = 'yaml'
    INI: const(str) = 'ini'
