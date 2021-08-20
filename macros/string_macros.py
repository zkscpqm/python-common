from types_extensions import tuple_type


def split_string(str_: str, index: int) -> tuple_type[str, str]:
    """
    Takes a string and returns a tuple of the string, split at the index given
    """
    if index >= len(str_):
        raise IndexError
    return str_[:index], str_[index:]
