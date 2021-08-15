from threading import Thread
from typing import Any, Iterable, Mapping

from types_extensions import Number_t, Function, void, safe_type


class CallbackThread(Thread):

    def __init__(self, group: void = None, target: Function = None, name: str = None,
                 args: Iterable[Any] = (), kwargs: Mapping[str, Any] = None, *, daemon: bool = None,
                 callback: Function = None, callback_extra_args: Iterable[Any] = (),
                 callback_extra_kwargs: Mapping[str, Any] = None) -> void:
        Thread.__init__(self, group=group, target=target, name=name,
                        args=args, kwargs=kwargs, daemon=daemon)
        self._target: Function = target
        self._args: Iterable[Any] = args
        self._kwargs: safe_type(Mapping[str, Any]) = kwargs or {}
        self._callback: Function = callback
        self._callback_extra_args: Iterable[Any] = callback_extra_args
        self._callback_extra_kwargs: safe_type(Mapping[str, Any]) = callback_extra_kwargs or {}

    def run(self) -> void:
        if self._target is not None:
            return_value = self._target(*self._args, **self._kwargs)
            if self._callback:
                self._callback(return_value, *self._callback_extra_args, **self._callback_extra_kwargs)
        del self._target, self._args, self._kwargs
