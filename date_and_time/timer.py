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


class Timer:

    def __init__(self, name: str = None) -> void:
        self.name = name or f'timer-{randrange(10000, 99999)}'
        self.start_time: safe_type(_dt) = None
        self.end_time: safe_type(_dt) = None
        self.is_running: bool = False
        self.splits: list[Split] = []

    def __enter__(self) -> 'Timer':
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
        last_split = self.split()
        self.is_running = False
        self.end_time = last_split.taken_at
        return last_split

    def split(self) -> Split:
        if not self.is_running:
            raise TimerNotRunningException

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
        self.start_time = _dt.now() if self.is_running else None
        self.splits = []
        self.end_time = None

    def __str__(self) -> str:
        return f"Timer(name={self.name} running_since: {self.start_time if self.is_running else 'not running'})"

    def __repr__(self) -> str:
        return str(self)


class TimerNotRunningException(Exception):

    def __str__(self) -> str:
        message = "The timer is not running! To do this, you need to call the start() method or use the context manager"
        return message
