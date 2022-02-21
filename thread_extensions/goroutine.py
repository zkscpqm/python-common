from threading import Thread, RLock
from typing import Any, Iterable, Mapping, Generator

from types_extensions import Function, void, safe_type, const, Number_t


class WaitGroup:
    """
    A waitgroup which behaves like Go's waitgroup object. A number of items to wait for can be incremented and
    decremented, and you can force a thread to wait until all waited items are done.
    """

    def __init__(self, items_to_wait: int = 0):
        self.waiting: int = items_to_wait

    def add(self, delta: int = 1):
        self.waiting += delta

    def wait(self):
        while self.waiting > 0:
            ...

    def done(self, delta: int = 1):
        self.waiting -= delta


class ChannelClosed(Exception):

    def __str__(self) -> str:
        return "This channel is closed. You can bypass this exception by passing `safe=True` to put()"


class Channel:
    """
    A multi-threaded buffered communication medium for GoRoutines.
    It can be polled, iterated-over, and closed (rendering it read-only)
    """

    def __init__(self) -> void:
        self._lock: RLock = RLock()
        self._buffer: list[Any] = []
        self._closed: bool = False

    @property
    def is_closed(self) -> bool:
        return self._closed

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._buffer)

    def put(self, obj: Any, safe: bool = True):
        """
        Adds a new object to the output buffer if the channel is not closed.
        If the channel is closed:
            If the safe option is True, it will gracefully return.
            If the safe option is False, an exception will be raised, notifying the user that the channel is closed.
        """
        with self._lock:
            if not self._closed:
                self._buffer.append(obj)
            else:
                if safe:
                    return
                raise ChannelClosed

    def poll(self, block: bool = True) -> Any:
        """
        A potentially-blocking operation to get the next value in the buffer.
        If the block operation is true, the polling thread will be locked until an item is placed in the buffer,
        otherwise it will return None.

        """
        while self.size == 0:
            if block:
                ...
            else:
                return
        with self._lock:
            return self._buffer.pop(0)

    def iter(self) -> Generator:
        """
        A continuous iterator of the Channel's buffer. This can read while items are being written.
        """
        while self.size > 0:
            yield self.poll(block=False)

    def __next__(self):
        return self.poll()

    def close(self) -> void:
        self._closed = True


class _GoThread(Thread):

    def __init__(self, channel: Channel, group: void = None, target: Function = None, name: str = None,
                 args: Iterable[Any] = (), kwargs: Mapping[str, Any] = None, *, daemon: bool = None) -> void:
        """
        Do not use directly! Use go() instead.
        """
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

    """
    A wrapper class for a goroutine's execution and its assigned channel.
    """

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


def go(func: Function, channel: Channel = None, *args, **kwargs) -> GoRoutine:
    """
    Main API for goroutines. You can pass a channel if needed, otherwise one will be created or you.
    If you wish to use the channel, you need to have an argument in your passed function/method called `channel` of
    type `Channel` and within your function you can use its methods (see `Channel`) and you can also have your own
    logic for whe you stop function execution based on signals received to the channel.

    Usage:

    >>> def my_async_func(x: int, y: int, channel: Channel):
    >>>     for i in range(x, y):
    >>>         if channel.is_closed:
    >>>             return
    >>>         print(f'Produced: {i}')
    >>>         channel.put(i)
    >>>
    >>>
    >>> chan = Channel()
    >>> routine = go(my_async_func, chan, 0, 10)
    >>> stop = False
    >>> while not stop:
    >>>     val = chan.poll()  # Can also do routine.poll() if you didn't specifically instantiate the channel
    >>>     print(f'Consumed: {val}')
    >>>     if val == 5:
    >>>         chan.close()  # Can also do routine.stop()

    Expected output:

    Produced: 0
    Consumed: 0
    Produced: 1
    Consumed: 1
    Produced: 2
    Consumed: 2
    Produced: 3
    Consumed: 3
    Produced: 4
    Consumed: 4
    Produced: 5
    Consumed: 5

    Note: Sometimes higher values can be produced (but not consumed) depending on the time to set the properties etc...
    """
    channel = channel or Channel()
    t_ = _GoThread(channel, target=func, args=args, kwargs=kwargs)
    t_.start()
    return GoRoutine(
        executor=t_,
        chan=channel
    )
