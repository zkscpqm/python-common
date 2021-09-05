from meta.config_meta import FinalConfigMeta
from types_extensions import const


class S3StorageClass(metaclass=FinalConfigMeta):
    STANDARD: const(str) = 'STANDARD'
    REDUCED_REDUNDANCY: const(str) = 'REDUCED_REDUNDANCY'
    STANDARD_IA: const(str) = 'STANDARD_IA'
    ONEZONE_IA: const(str) = 'ONEZONE_IA'
    INTELLIGENT_TIERING: const(str) = 'INTELLIGENT_TIERING'
    GLACIER: const(str) = 'GLACIER'
    DEEP_ARCHIVE: const(str) = 'DEEP_ARCHIVE'
    OUTPOSTS: const(str) = 'OUTPOSTS'
