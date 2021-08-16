import random
from typing import Iterable

from context.context import GlobalContextTable
from types_extensions import void, const


class UIDGenerator:

    _DEFAULT_CHARSET: str = "abcdefghijklmnopqrstuvwxyz1234567890"
    CONTEXT_KEY: const(str) = "active_global_uids"

    def __init__(self, length: int = 8, charset: str | Iterable[str] = None) -> void:

        self.length: int = length
        self.charset: str | Iterable[str] = charset or self._DEFAULT_CHARSET

    def new(self) -> str:
        with GlobalContextTable() as ctx:
            active_uids = ctx.get(self.CONTEXT_KEY)
            uid_set: set[str] = active_uids.get_current_data() if active_uids else set()
            unique = False
            while not unique:
                rv_ = ""
                for _ in range(self.length):
                    rv_ += self.charset[random.randint(0, len(self.charset) - 1)]
                if rv_ not in uid_set:
                    unique = True
                    uid_set.add(rv_)
            ctx.upsert(self.CONTEXT_KEY, uid_set, preserve_old_data=False)

        return rv_

    def deregister(self, uid: str) -> void:
        with GlobalContextTable() as ctx:
            active_uids = ctx.get(self.CONTEXT_KEY)
            if active_uids:
                uid_set: set[str] = active_uids.get_current_data()
                try:
                    uid_set.remove(uid)
                    ctx.upsert(self.CONTEXT_KEY, uid_set, preserve_old_data=False)
                except KeyError:
                    pass
