from version_checking import _assert_py_version, PythonVersion

_assert_py_version(PythonVersion(3, 10))

import abc
import warnings
from typing import Any
from datetime import datetime as _dt

from meta.singleton_meta import SingletonMeta, ThreadLocalSingletonMeta
from types_extensions import void, const


class ContextEntryData:
    """
    A versioned registry entry. It contains a list of historical data and changelogs to log when changes were made.
    The changelog always persists, while the data is only versioned when needed.
    """

    def __init__(self, key: Any, data: Any) -> void:
        self.key: Any = key
        self.data: list[Any] = [data]
        self.created_at: const(_dt) = _dt.now()
        self.changelog: list[_dt] = [self.created_at]

    def get_current_data(self) -> Any:
        """
        :return: Latest version of the data for this entry
        """
        return self.data[-1]

    def __str__(self) -> str:
        return str(self.get_current_data())


class _ContextEntry:
    """
    This should never be visible in any downstream app. It exists to abstract the update() method from people using
    a context table.
    """

    def __init__(self, key: Any, data: Any) -> void:
        self._data = ContextEntryData(key=key, data=data)

    def update(self, new_data: Any, preserve_old_data: bool) -> void:
        previous_idx = len(self._data.data) - 1
        if not preserve_old_data:
            self.data.data[previous_idx] = None
        self.data.data.append(new_data)
        self.data.changelog.append(_dt.now())

    @property
    def data(self) -> ContextEntryData:
        return self._data


class ContextTable(metaclass=abc.ABCMeta):
    """
    Base class for context tables. Don't use this directly. Use GlobalContextTable or ThreadLocalContextTable
    depending on the use case
    """

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
        """
        :param key: Self explanatory
        :param value: Self explanatory
        :param preserve_old_data: If set to true and the key exists, its old value will not be deleted and will be
        accessible via the entry.
        """
        key = self.define_key(key)
        if key not in self._table:
            self._table[key] = _ContextEntry(key=key, data=value)
        else:
            self._table[key].update(value, preserve_old_data)

    def delete(self, key: Any, preserve_old_data: bool = False) -> void:
        """
        :param key: Self explanatory
        :param preserve_old_data: If set to true and the key exists, its old value will not be deleted and will be
        accessible via the entry.
        """
        key = self.define_key(key)
        if not preserve_old_data:
            del self._table[key]
        else:
            if key in self._table:
                self.upsert(key=key, value=void, preserve_old_data=preserve_old_data)

    @staticmethod
    def define_key(key: Any) -> Any:
        """
        Determine if a given key is hashable. This prevents errors when trying to use things like lists or sets as
        keys in the registry. If the latter occurs, a warning is shown to alert the user the key they gave is not what
        will be used as a key in the registry.

        :param key: A potential key to use
        :return: The same key if it's hashable, otherwise its string representation.
        """
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
