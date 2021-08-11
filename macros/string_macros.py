

def split_string(str_: str, index: int) -> tuple[str, str]:
    if index >= len(str_):
        raise IndexError
    return str_[:index], str_[index:]
