import json
from typing import Any

from io_extensions.file_extensions import FileExtensions
from io_extensions.file_rw import safe_fwrite
from types_extensions import void, primitives, single_value_iterables, is_of_type, Method, list_type, dict_type


class ObjectSerializer:

    def __init__(self, default_serialization: str = None) -> void:
        self.default_serialization = default_serialization or FileExtensions.JSON

    @staticmethod
    def _is_magic_member(member_name: str) -> bool:
        return member_name.startswith('__') and member_name.endswith('__')

    @staticmethod
    def _is_method(value: Any) -> bool:
        return isinstance(value, Method)

    @classmethod
    def _should_process(cls, obj: Any, member_name: str, include_magic_members: bool = False,
                        include_methods: bool = True) -> bool:
        if not include_magic_members:
            if cls._is_magic_member(member_name):
                return False
        if not include_methods:
            if cls._is_method(getattr(obj, member_name, None)):
                return False
        return True

    @classmethod
    def _create_filtered_list_from_iterable(cls, iterable: single_value_iterables, include_magic_members: bool = False,
                                            include_methods: bool = True, file_safe: bool = False) -> list_type:
        rv = []
        for item in iterable:
            if not include_methods and cls._is_method(item):
                continue
            rv.append(cls.to_dict(item, include_magic_members, include_methods, file_safe))
        return rv

    @classmethod
    def _create_filtered_dict(cls, input_dict: dict, include_magic_members: bool = False,
                              include_methods: bool = True, file_safe: bool = False) -> dict_type:
        rv = {}
        for key, value in input_dict.items():
            if not include_methods and (cls._is_method(key) or cls._is_method(value)):
                continue
            new_key = cls.to_dict(key, include_magic_members, include_methods, file_safe)
            try:
                hash(new_key)
            except TypeError:
                new_key = str(new_key)
            rv[new_key] = cls.to_dict(value, include_magic_members, include_methods, file_safe)
        return rv

    @classmethod
    def to_dict(cls, obj: Any, include_magic_members: bool = False,
                include_methods: bool = True, file_safe: bool = False) -> Any:
        try:
            match type(obj):
                case x if is_of_type(x, primitives):
                    return obj
                case x if is_of_type(x, single_value_iterables):
                    return cls._create_filtered_list_from_iterable(x, include_magic_members, include_methods, file_safe)
                case x if is_of_type(x, dict):
                    return {
                        cls.to_dict(key, include_magic_members, include_methods, file_safe):
                            cls.to_dict(value, include_magic_members, include_methods, file_safe)
                        for key, value in x.items()
                    }
                case _ if callable(obj):
                    if include_methods:
                        return obj if not file_safe else str(obj)

            rv = {}
            members = dir(obj)
            for member_name in members:
                if not include_magic_members and cls._is_magic_member(member_name):
                    continue
                attr_ = getattr(obj, member_name, None)
                if not include_methods and isinstance(attr_, Method):
                    continue
                rv[member_name] = cls.to_dict(attr_, include_magic_members, include_methods, file_safe)
            return rv

        except Exception:
            return

    def serialize(self, obj: Any, format_: str = None,  include_magic_members: bool = False,
                  include_methods: bool = True, destination_fp: str = None,  **serializer_kwargs) -> str:
        format_ = format_ or self.default_serialization
        as_dict = self.to_dict(obj, include_magic_members, include_methods, file_safe=True)
        rv = self._serialize(as_dict, format_, **serializer_kwargs)
        if destination_fp:
            safe_fwrite(destination_fp, mode='w+', payload=rv)
        return rv

    @staticmethod
    def _serialize(obj_dict: dict[str: Any], format_: str, **serializer_kwargs) -> str:

        match format_:
            case fmt if fmt == FileExtensions.JSON:
                return json.dumps(obj_dict, indent=4, **serializer_kwargs)
            case fmt if fmt == FileExtensions.YAML:
                import yaml
                return yaml.safe_dump(obj_dict, **serializer_kwargs)
            case fmt if fmt == FileExtensions.XML:
                from dict2xml import dict2xml
                return dict2xml(obj_dict, **serializer_kwargs)
        return ''
