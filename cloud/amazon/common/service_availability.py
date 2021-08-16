from types_extensions import const

from meta.config_meta import FinalConfigMeta


class ServiceAvailability(metaclass=FinalConfigMeta):

    OFFLINE: const(int) = 0
    ONLINE: const(int) = 1
    CONNECTED: const(int) = 2
