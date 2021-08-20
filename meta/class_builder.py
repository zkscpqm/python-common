from typing import Iterable, Any

from types_extensions import void, tuple_type, dict_type, list_type


class DynamicClassFactory:
    """
    A factory to dynamically create classes (not instances).

    Tbh I made this because I can, not because I've ever needed anything like it. If anyone ends up using this,
    let me know the use-case at: zkscpqm@daum.net

    """

    def __init__(self, default_base_classes: Iterable[type] = (), prefix: str = '', suffix: str = '',
                 members: dict_type[str, Any] = None) -> void:
        """
        :param default_base_classes: A collection of base classes to be inherited-from by any classes built by this
        :param prefix: A global prefix to be tagged onto the name of any classes built by this
        :param suffix: A global suffix to be tagged onto the name of any classes built by this
        :param members: A collection of attributes/methods (name -> attribute) to be implemented by any classes built by this
        """
        self.prefix: str = prefix
        self.suffix: str = suffix
        self.mixins: list_type[type] = [x for x in default_base_classes]
        self.members: dict_type[str, Any] = members or {}

    def build(self, class_name: str, extra_mixins: Iterable[type] = (),
              members: dict_type[str, Any] = None) -> type:
        """

        :param class_name: What sits in between the configured prefix and suffix
        :param extra_mixins: More base classes
        :param members: More members. Note there are no checks performed so you can have an attribute like "??my-attr."
        :return: Your shiny new class!
        """
        name_ = self.prefix + class_name + self.suffix
        return type(
            name_,
            self._create_bases(extra_base_classes=extra_mixins),
            {**self.members, **(members or {})}
        )

    def _create_bases(self, extra_base_classes: Iterable[type]) -> tuple_type[type]:
        """
        This shit is necessary because type() *needs* a tuple instead of a list or any other ordered collection
        """
        return tuple(self.mixins + [x for x in extra_base_classes])
