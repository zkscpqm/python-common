from abc import ABCMeta, abstractmethod
from typing import Iterable, Union

from types_extensions import void, Number_t, safe_type, list_type, tuple_type


class HeapEntry(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, i: Number_t) -> void:
        self.i: Number_t = i

    def _iter_filtered_members(self) -> Iterable[tuple_type[str, str]]:
        ignored_members = {'_iter_filtered_members', 'i'}
        for k, v in self.__dict__.items():
            if not (k.startswith('__') and k.endswith('__')) and k not in ignored_members:
                yield k, v

    def __str__(self) -> str:
        return f"[{self.i}] {', '.join(f'{k}=>{v}' for k, v in self._iter_filtered_members())}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Union['HeapEntry', Number_t]) -> bool:
        if isinstance(other, Number_t):
            return self.i == other
        return self.i == other.i

    def __lt__(self, other: Union['HeapEntry', Number_t]) -> bool:
        if isinstance(other, Number_t):
            return self.i < other
        return self.i < other.i

    def __le__(self, other: Union['HeapEntry', Number_t]) -> bool:
        if isinstance(other, Number_t):
            return self.i <= other
        return self.i <= other.i


class MaxHeap:
    """
    Heap struct with a list backend. Expects entries subclassed from HeapEntry. Can be initialized with an existing
    unsorted list or empty. Inserts/deletes auto-heapify.
    """

    def __init__(self, data: list_type[HeapEntry] = None):
        self.data: list_type[HeapEntry] = data or []
        self.heapsort()

    @property
    def heap_size(self) -> int:
        return len(self.data)

    def heapsort(self) -> void:
        iterations = range(self.heap_size // 2 - 1, -1, -1)
        for i in iterations:
            self.max_heapify(i)

    def max_heapify(self, root_idx: int = 0) -> void:
        left = self._left(root_idx)
        right = self._right(root_idx)
        largest_idx = root_idx
        if left < self.heap_size and self.data[left] > self.data[largest_idx]:
            largest_idx = left

        if right < self.heap_size and self.data[right] > self.data[largest_idx]:
            largest_idx = right

        if largest_idx != root_idx:
            # If the tree is unbalanced in some way, float the initial root index down and heapify again
            self.data[root_idx], self.data[largest_idx] = self.data[largest_idx], self.data[root_idx]
            self.max_heapify(largest_idx)

    def insert(self, value: HeapEntry) -> void:
        self.data.insert(0, value)
        self.heapsort()

    def pop(self) -> HeapEntry:
        v = self.data.pop(0)
        self.heapsort()
        return v

    def peek(self) -> safe_type(HeapEntry):
        if self.heap_size > 0:
            return self.data[0]
        return

    @staticmethod
    def _left(idx: int) -> int:
        return (idx << 0x01) + 1

    @staticmethod
    def _right(idx: int) -> int:
        return (idx << 0x01) + 2

    @staticmethod
    def _parent(idx: int) -> int:
        if idx & 0x0:
            return idx
        return idx >> 0x01

    def __len__(self) -> int:
        return self.heap_size

    def __getitem__(self, idx: int) -> HeapEntry:
        return self.data[idx]

    def __setitem__(self, key: int, value: HeapEntry) -> void:
        self.data[key] = value
        self.heapsort()

    def __str__(self) -> str:
        return str(self.data)
