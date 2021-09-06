from meta.config_meta import FinalConfigMeta
from types_extensions import const, void


class DateFormatting(metaclass=FinalConfigMeta):
    DDMMYYYY: const(str) = '%d%m%Y'
    YYYYMMDD: const(str) = '%Y%m%d'
    DDMMYYYY_dash_delimited: const(str) = '%d-%m-%Y'
    YYYYMMDD_dash_delimited: const(str) = '%Y-%m-%d'
    DDMMYYYY_space_delimited: const(str) = '%d %m %Y'
    YYYYMMDD_space_delimited: const(str) = '%Y %m %d'


class TimeFormatting(metaclass=FinalConfigMeta):
    HHMMSS: const(str) = '%H%M%S'
    HHMMSS_dash_delimited: const(str) = '%H-%M-%S'
    HHMMSS_space_delimited: const(str) = '%H %M %S'
    HHMMSSms: const(str) = '%H%M%S%f'
    HHMMSSms_dash_delimited: const(str) = '%H-%M-%S-%f'
    HHMMSSms_space_delimited: const(str) = '%H %M %S %f'


class DTFormatter(DateFormatting, TimeFormatting):

    DT_DELIMITER: str = ' '

    def __init__(self, delimiter: str = ' ') -> void:
        if delimiter:
            self.DT_DELIMITER = delimiter

    def default_time_first(self) -> str:
        return f"{self.HHMMSS_dash_delimited}{self.DT_DELIMITER}{self.DDMMYYYY_dash_delimited}"

    def default_date_indexed(self) -> str:
        return f"{self.YYYYMMDD_dash_delimited}{self.DT_DELIMITER}{self.HHMMSS_dash_delimited}"
