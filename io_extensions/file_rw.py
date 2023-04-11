import os

from types_extensions import string_like


def safe_make_dirs(path: str):
    path = os.path.dirname(path) or '.'
    os.makedirs(path, exist_ok=True)


def safe_fwrite(filepath: str, payload: string_like,  mode: str = 'w+', **kwargs):
    safe_make_dirs(filepath)
    if mode == 'w':
        mode = 'w+'
    if mode == 'wb':
        mode = 'wb+'

    with open(filepath, mode, **kwargs) as file_h:
        file_h.write(payload)
