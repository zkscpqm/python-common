import abc
import warnings
from typing import Any
from datetime import datetime as _dt

from meta.singleton_meta import SingletonMeta, ThreadLocalSingletonMeta
from types_extensions import void, const


class ContextEntryData:

    def __init__(self, key: Any, data: Any) -> void:
        self.key: Any = key
        self.data: list[Any] = [data]
        self.created_at: const(_dt) = _dt.now()
        self.changelog: list[_dt] = [self.created_at]

    def get_current_data(self) -> Any:
        return self.data[-1]

    def __str__(self) -> str:
        return str(self.get_current_data())


class _ContextEntry:

    def __init__(self, key: Any, data: Any) -> void:
        self._data = ContextEntryData(key=key, data=data)

    def update(self, new_data: Any, preserve_old_data: bool) -> void:
        previous_idx = len(self._data.data) - 1
        if not preserve_old_data:
            self.data.data[previous_idx] = void
        self.data.data.append(new_data)
        self.data.changelog.append(_dt.now())

    @property
    def data(self) -> ContextEntryData:
        return self._data


class ContextTable(metaclass=abc.ABCMeta):

    def __init__(self) -> void:
        self._table: dict[Any, _ContextEntry] = {}

    def __enter__(self) -> 'ContextTable':
        return self

    def __exit__(self, _, __, ___) -> void:
        pass

    def exists(self, key: Any) -> bool:
        key = self.define_key(key)
        return key in self._table

    def get(self, key: Any) -> ContextEntryData:
        key = self.define_key(key)
        if entry := self._table.get(key):
            return entry.data

    def upsert(self, key: Any, value: Any, preserve_old_data: bool = False) -> void:
        key = self.define_key(key)
        if key not in self._table:
            self._table[key] = _ContextEntry(key=key, data=value)
        else:
            self._table[key].update(value, preserve_old_data)

    def delete(self, key: Any, preserve_old_data: bool = False) -> void:
        key = self.define_key(key)
        if not preserve_old_data:
            del self._table[key]
        else:
            if key in self._table:
                self.upsert(key=key, value=void, preserve_old_data=preserve_old_data)

    @staticmethod
    def define_key(key: Any) -> Any:
        try:
            hash(key)
        except ValueError:
            warnings.warn(f"The given key: {key} cannot be hashed, so it is stored by its str() representation instead")
            key = str(key)
        return key

    def __setitem__(self, key: Any, value: Any) -> void:
        self.upsert(key, value)

    def __delitem__(self, key: Any) -> void:
        del self._table[key]

    def __getitem__(self, key: Any) -> ContextEntryData:
        return self.get(key)


class GlobalContextTable(ContextTable, metaclass=SingletonMeta):
    pass


class ThreadLocalContextTable(ContextTable, metaclass=ThreadLocalSingletonMeta):
    pass
