from datetime import datetime as _dt, timedelta
from random import randrange

from types_extensions import void, safe_type, Final


class Split:

    def __init__(self, taken_at: _dt, since_start: timedelta, since_last_split: timedelta) -> void:
        self.taken_at: Final[_dt] = taken_at
        self.since_start: Final[timedelta] = since_start
        self.since_last_split: Final[timedelta] = since_last_split

    def __str__(self) -> str:
        return f"Split(<{self.taken_at}>, since_start={self.since_start}, since_last_split={self.since_last_split})"

    def __repr__(self) -> str:
        return str(self)


class Stopwatch:

    def __init__(self, name: str = void) -> void:
        self.name: str = name or f'stopwatch-{randrange(10000, 99999)}'
        self.start_time: safe_type(_dt) = void
        self.end_time: safe_type(_dt) = void
        self.is_running: bool = False
        self.splits: list[Split] = []

    def __enter__(self) -> 'Stopwatch':
        self.start()
        return self

    def __exit__(self, *a, **k) -> void:
        self.stop()

    def start(self, reset_stats: bool = True) -> void:
        if reset_stats:
            self.end_time = void
            self.splits = []
        self.start_time = _dt.now()
        self.is_running = True

    def stop(self) -> Split:
        last_split = self.split()
        self.is_running = False
        self.end_time = last_split.taken_at
        return last_split

    def split(self) -> Split:
        if not self.is_running:
            raise StopwatchNotRunningException

        now_ = _dt.now()
        last_split_time = self.splits[-1].taken_at if self.splits else self.start_time

        new_split = Split(taken_at=now_,
                          since_start=now_ - self.start_time,
                          since_last_split=now_ - last_split_time)
        self.splits.append(new_split)
        return new_split

    def reset(self, stop: bool = False) -> void:
        if stop:
            self.stop()
        self.start_time = _dt.now() if self.is_running else void
        self.splits = []
        self.end_time = void

    def __str__(self) -> str:
        return f"Stopwatch(name={self.name} running_since: {self.start_time if self.is_running else 'not running'})"

    def __repr__(self) -> str:
        return str(self)


class StopwatchNotRunningException(Exception):

    def __str__(self) -> str:
        message = "The stopwatch is not running!" \
                  "To do this, you need to call the start() method or use the context manager"
        return message