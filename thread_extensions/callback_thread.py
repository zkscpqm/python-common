from threading import Thread
from typing import Any, Iterable, Mapping

from types_extensions import Function, void, safe_type


class CallbackThread(Thread):
    """
    An extension to python's threading API allowing for a callback to be executed upon completion of the given
    function. The callback is executed with the initial function's return value as the first parameter and any other
    givent args and kwargs following.

    Usage:

    >>> def callback_func(x: int, y: int) -> None:
    >>>
    >>>     print(f'Called with {x=} and {y=}.')
    >>>
    >>> def func(x: int) -> int:
    >>>     return x + 1

    >>> thread_ = CallbackThread(target=func, kwargs={'x': 10}, callback=callback_func, callback_extra_args=(7,))
    >>> thread_.start()
    >>> thread_.join()

    ----
    Called with x=11 and y=7

    """

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
        if self._target:
            return_value = self._target(*self._args, **self._kwargs)
            if self._callback:
                self._callback(return_value, *self._callback_extra_args, **self._callback_extra_kwargs)
        del self._target, self._args, self._kwargs
