import time
from datetime import datetime as _dt
from typing import Iterable
from threading import Thread

from types_extensions import Number_t, safe_type, Function, void


class _TimerThread(Thread):

    def __init__(self, timeout: Number_t, *, repetitions: int, callbacks: Iterable[Function],
                 callback_args: tuple, callback_kwargs: dict, name: str = None) -> void:
        Thread.__init__(self, name=name)
        self.timeout: Number_t = timeout
        self.repetitions: int = repetitions
        self.stopped = False
        self.paused = False
        self.elapsed: float = 0.
        self.started_at: safe_type(_dt) = None
        self._callbacks: Iterable[Function] = callbacks
        self._callback_args: tuple = callback_args
        self._callback_kwargs: dict = callback_kwargs

    def stop(self) -> void:
        self.stopped = True

    def restart(self) -> void:
        self.stopped = False
        self.paused = False
        self.run()

    def pause(self) -> void:
        self.paused = True

    def unpause(self) -> void:
        self.paused = False

    def start(self):
        self.started_at = _dt.now()
        Thread.start(self)

    def run(self) -> void:
        for current in range(self.repetitions):
            sleep_times = self.timeout * 10
            for sleep_number in range(sleep_times):
                if self.stopped:
                    break
                while self.paused:
                    ...
                time.sleep(0.1)
                self.elapsed += 0.1
            if self.stopped:
                self.repetitions -= current
                break

            for callback in self._callbacks:
                if self.stopped:
                    break
                callback(*self._callback_args, **self._callback_kwargs)

    def force_join(self, timeout: float) -> void:
        self.stop()
        return self.join(timeout)


class Timer:

    def __init__(self, timeout: Number_t, *, repetitions: int = 1, callbacks: Iterable[Function] = (),
                 callback_args: tuple = (), callback_kwargs: dict = None) -> void:
        self.is_running: bool = False
        self._thread: _TimerThread = self._create_thread(timeout,
                                                         repetitions=repetitions,
                                                         callbacks=callbacks,
                                                         callback_args=callback_args,
                                                         callback_kwargs=callback_kwargs or {})

    @staticmethod
    def _create_thread(timeout: Number_t, repetitions: int, callbacks: Iterable[Function],
                       callback_args: tuple, callback_kwargs: dict) -> _TimerThread:
        return _TimerThread(timeout, repetitions=repetitions, callbacks=callbacks,
                            callback_args=callback_args, callback_kwargs=callback_kwargs)

    def start(self) -> void:
        self.is_running = True
        self._thread.start()

    def elapsed(self) -> float:
        return self._thread.elapsed

    def started_at(self) -> safe_type(_dt):
        return self._thread.started_at

    def pause(self) -> void:
        self._thread.pause()

    def unpause(self) -> void:
        self._thread.unpause()

    def force_join(self, timeout: float = None) -> void:
        self._thread.force_join(timeout)
