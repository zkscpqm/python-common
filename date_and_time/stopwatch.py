from datetime import datetime as _dt, timedelta
from random import randrange
import warnings

from types_extensions import void, safe_type, const, list_type


class Split:
    """
    Struct used by the Stopwatch. Best not to use it directly.
    """

    def __init__(self, taken_at: _dt, since_start: timedelta, since_last_split: timedelta) -> void:
        """
        :param taken_at: The exact datetime of when the split was made
        :param since_start: Time difference between when the stopwatch started and the time the split was made
        :param since_last_split: Time difference between this and the previous split
        (if such exists, otherwise since start)
        """
        self.taken_at: const(_dt) = taken_at
        self.since_start: const(timedelta) = since_start
        self.since_last_split: const(timedelta) = since_last_split

    def __str__(self) -> str:
        return f"Split(<{self.taken_at}>, since_start={self.since_start}, since_last_split={self.since_last_split})"

    def __repr__(self) -> str:
        return str(self)


class Stopwatch:
    """
    A class which counds UP when its start() method is called until the stop() method is called.
    Calling pause() and unpause() will create blocks of time to be removed from both the active split and total runtime

    Usage:
    >>> import time
    >>>
    >>> with Stopwatch() as s:
    >>>     time.sleep(5)  # Stopwatch is running, 5 seconds added to current (first) split
    >>>     s.pause()
    >>>     time.sleep(2)  # This time will be taken away from the first split (and subsequently, total runtime)
    >>>     s.split(force=True)  # The current split is finalized and a new one is started. Since it was paused,
    >>>                          # this force unpauses upon starting the new split.
    >>>     time.sleep(3)  # Stopwatch is running, 3 seconds added to current (second) split
    >>>     s.pause()
    >>>     time.sleep(1)  # This time will be taken away from the second split (and subsequently, total runtime)
    >>>     s.unpause()
    >>>     time.sleep(3)  # Stopwatch is running, 3 seconds added to current (second) split
    >>>
    >>> assert s.elapsed == 5 + 3 + 3  # Give or take a few ms

    """

    def __init__(self, name: str = None) -> void:
        self.name: str = name or f'stopwatch-{randrange(10000, 99999)}'
        self.start_time: safe_type(_dt) = None
        self.end_time: safe_type(_dt) = None
        self.is_running: bool = False
        self._paused_at: safe_type(_dt) = None
        self._paused_for_total: float = 0.
        self._paused_for_this_split: float = 0.
        # List containing all splits in order. If stopped, the last split will always be the end_time.
        self.splits: list_type[Split] = []

    @property
    def elapsed(self) -> timedelta:
        if self.is_running:
            return (_dt.now() - self.start_time) - self._paused_for_total
        if self.start_time:
            return (self.end_time - self.start_time) - self._paused_for_total

    def __enter__(self) -> 'Stopwatch':
        self.start()
        return self

    def __exit__(self, *a, **k) -> void:
        self.stop()

    def start(self, reset_stats: bool = True) -> void:
        if reset_stats:
            self.end_time = None
            self.splits = []
        self.start_time = _dt.now()
        self.is_running = True

    def stop(self) -> Split:
        last_split = self.split(force=True)
        self.is_running = False
        self.end_time = last_split.taken_at
        return last_split

    def pause(self):
        if not self._paused_at and self.is_running:
            self._paused_at = _dt.now()

    def unpause(self):
        if self._paused_at:
            pause_duration = _dt.now() - self._paused_at
            self._paused_for_this_split += pause_duration
            self._paused_for_total += pause_duration
            self._paused_at = None

    def split(self, force: bool = False) -> safe_type(Split):
        if not self.is_running:
            raise StopwatchNotRunningException
        if self._paused_at is not None:
            if not force:
                warnings.warn("The stopwatch is paused, so a split has not been made.")
                return
            self.unpause()

        now_ = _dt.now()
        last_split_time = self.splits[-1].taken_at if self.splits else self.start_time

        new_split = Split(taken_at=now_,
                          since_start=(now_ - self.start_time) - self._paused_for_total,
                          since_last_split=(now_ - last_split_time) - self._paused_for_this_split)
        self.splits.append(new_split)
        self._paused_for_this_split = 0.
        return new_split

    def reset(self, stop: bool = False) -> void:
        if stop:
            self.stop()
        self.start_time = _dt.now() if self.is_running else void
        self.splits = []
        self.end_time = None
        self._paused_for_total = 0.
        self._paused_for_this_split = 0.
        self._paused_at = None

    def __str__(self) -> str:
        return f"Stopwatch(name={self.name} running_since: {self.start_time if self.is_running else 'not running'}, " \
               f"elapsed={self.elapsed})"

    def __repr__(self) -> str:
        return str(self)


class StopwatchNotRunningException(Exception):

    def __str__(self) -> str:
        message = "The stopwatch is not running!" \
                  "To do this, you need to call the start() method or use the context manager"
        return message
