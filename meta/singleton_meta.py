
class SingletonMeta(type):
    """
    Metaclass for defining classes which should only have a single active instance. This kind of thing is considered an
    antipattern and can cause very annoying bugs when testing so only use it if you know what you're doing.

    The instances are stored in a dict like `ClassName -> InstanceOf` and they persist between threads!

    Usage:

    >>> class MySingletonClass(metaclass=SingletonMeta):
    >>>
    >>>     def __init__(self):
    >>>         print('Constructor called!')
    >>>
    >>> inst_1 = MySingletonClass()
    >>> inst_2 = MySingletonClass()
    >>> print(inst_1 is inst_2)
    ---
    Constructor called!
    True
    ---
    In the case above, the cached instances will look something like:
    {
        'MySingletonClass': <__main__.MySingletonClass object at 0x0000014FA85E3670>
    }

    """

    _instances: dict[str, object] = {}

    def __call__(cls, *args, **kwargs) -> object:
        if cls.__name__ not in cls._instances:
            cls._instances[cls.__name__] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls.__name__]


class ThreadLocalSingletonMeta(type):
    """
    Metaclass for defining classes which should only have a single active instance per thread. This kind of thing is
    considered an antipattern and can cause very annoying bugs when testing so only use it if you know what you're
    doing.

    The instances are stored here in a dict residing in locals() under a key: '__singleton_instances'
    The mapping looks like `ClassName -> InstanceOf`

    Usage:

    >>> import threading
    >>> class MySingletonClass(metaclass=SingletonMeta):
    >>>
    >>>     def __init__(self, instance_number: int):
    >>>         print(f'Constructor called for {instance_number=}!')
    >>>
    >>> inst_1 = MySingletonClass(1)
    >>> inst_2 = MySingletonClass(2)
    >>> threading.Thread(target=MySingletonClass, args=(3,))
    >>> print(inst_1 is inst_2)
    ---
    Constructor called for instance_number=1!
    Constructor called for instance_number=3!
    True
    ---
    In the case above, the cached instances will look something like:
    {
        'MySingletonClass': <__main__.MySingletonClass object at 0x0000014FA85E3670>
    }

    """

    _locals_key: str = "__singleton_instances"

    def __call__(cls, *args, **kwargs) -> object:
        if not locals().get(cls._locals_key):
            locals()[cls._locals_key]: dict[str, object] = {}
        if cls.__name__ not in locals()[cls._locals_key]:
            locals()[cls._locals_key][cls.__name__] = super(ThreadLocalSingletonMeta, cls).__call__(*args, **kwargs)
        return locals()[cls._locals_key][cls.__name__]
