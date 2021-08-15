from threading import Thread
from typing import Any, Iterable, Mapping

from types_extensions import Number_t, Function, void, safe_type


class ReturnValueThread(Thread):

    def __init__(self, group: void = None, target: Function = None, name: str = None,
                 args: Iterable[Any] = (), kwargs: Mapping[str, Any] = None, *, daemon: bool = None) -> void:
        Thread.__init__(self, group=group, target=target, name=name,
                        args=args, kwargs=kwargs, daemon=daemon)
        self._target: Function = target
        self._args: Iterable[Any] = args
        self._kwargs: safe_type(Mapping[str, Any]) = kwargs or {}
        self.return_value: Any = None
        self.finished: bool = False

    def run(self) -> void:
        if self._target is not None:
            self.return_value = self._target(*self._args, **self._kwargs)
        self.finished = True
        del self._target, self._args, self._kwargs

    def join(self, timeout: Number_t = None) -> Any:
        Thread.join(self, timeout)
        return self.return_value
