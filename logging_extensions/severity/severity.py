import dataclasses

from types_extensions import const


@dataclasses.dataclass
class Severity:
    text: const(str)
    level: const(int)

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: 'Severity'):
        return self.level == other.level

    def __gt__(self, other: 'Severity'):
        return self.level > other.level

    def __ge__(self, other: 'Severity'):
        return self.level >= other.level
