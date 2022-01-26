from threading import Thread
from typing import Any, Iterable, Mapping, Generator

from types_extensions import Function, void, safe_type, const, Number_t


class ChannelClosed(Exception):

    def __str__(self) -> str:
        return "This channel is closed. You can bypass this exception by passing `safe=True` to put()"


class Channel:

    def __init__(self) -> void:
        self._buffer: list[Any] = []
        self._closed: bool = False

    @property
    def is_closed(self) -> bool:
        return self._closed

    @property
    def size(self) -> int:
        return len(self._buffer)

    def put(self, obj: Any, safe: bool = True):
        if not self._closed:
            self._buffer.append(obj)
        else:
            if safe:
                return
            raise ChannelClosed

    def poll(self, block: bool = True) -> Any:
        while self.size == 0:
            if block:
                ...
            else:
                return
        return self._buffer.pop(0)

    def iter(self) -> Generator:
        while self.size > 0:
            yield self.poll(block=False)

    def close(self) -> void:
        self._closed = True


class _GoThread(Thread):

    def __init__(self, channel: Channel, group: void = None, target: Function = None, name: str = None,
                 args: Iterable[Any] = (), kwargs: Mapping[str, Any] = None, *, daemon: bool = None) -> void:
        Thread.__init__(self, group=group, target=target, name=name,
                        args=args, kwargs=kwargs, daemon=daemon)
        self._target: Function = target
        self._args: Iterable[Any] = args
        self._kwargs: safe_type(Mapping[str, Any]) = kwargs or {}
        self._kwargs['channel'] = channel
        self.finished: bool = False

    def run(self) -> void:
        if self._target is not None:
            try:
                self._target(*self._args, **self._kwargs)
            except TypeError:
                del self._kwargs['channel']
                self._target(*self._args, **self._kwargs)
        self.finished = True
        del self._target, self._args, self._kwargs


class GoRoutine:

    def __init__(self, executor: _GoThread, chan: Channel) -> void:
        self.__executor: const(_GoThread) = executor
        self.channel: const(Channel) = chan

    @property
    def is_finished(self) -> bool:
        return self.__executor.finished

    def poll(self, block: bool = True) -> Any:
        return self.channel.poll(block)

    def stop(self, timeout: Number_t = None) -> void:
        self.channel.close()
        self.__executor.join(timeout)


def go(func: Function, *args, **kwargs) -> GoRoutine:
    channel = Channel()
    t_ = _GoThread(channel, target=func, args=args, kwargs=kwargs)
    t_.start()
    return GoRoutine(
        executor=t_,
        chan=channel
    )
