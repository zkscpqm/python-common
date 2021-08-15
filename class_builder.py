from typing import Iterable, Any

from types_extensions import void


class DynamicClassFactory:

    def __init__(self, default_base_classes: Iterable[type] = (), prefix: str = '', suffix: str = '',
                 attributes: dict[str, Any] = None) -> void:
        self.prefix: str = prefix
        self.suffix: str = suffix
        self.mixins: list[type] = [x for x in default_base_classes]
        self.attributes: dict[str, Any] = attributes or {}

    def build(self, class_name: str, extra_mixins: Iterable[type] = (),
              attributes: dict[str, Any] = None) -> type:
        name_ = self.prefix + class_name + self.suffix
        return type(
            name_,
            self._create_bases(extra_base_classes=extra_mixins),
            {**self.attributes, **(attributes or {})}
        )

    def _create_bases(self, extra_base_classes: Iterable[type]) -> tuple[type]:
        return tuple(self.mixins + [x for x in extra_base_classes])
