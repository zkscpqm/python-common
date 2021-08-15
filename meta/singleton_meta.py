
class SingletonMeta(type):

    _instances: dict[str, object] = {}

    def __call__(cls, *args, **kwargs) -> object:
        if cls.__name__ not in cls._instances:
            cls._instances[cls.__name__] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls.__name__]


class ThreadLocalSingletonMeta(type):

    _locals_key: str = "__singleton_instances"

    def __call__(cls, *args, **kwargs) -> object:
        if not locals().get(cls._locals_key):
            locals()[cls._locals_key]: dict[str, object] = {}
        if cls.__name__ not in locals()[cls._locals_key]:
            locals()[cls._locals_key][cls.__name__] = super(ThreadLocalSingletonMeta, cls).__call__(*args, **kwargs)
        return locals()[cls._locals_key][cls.__name__]
