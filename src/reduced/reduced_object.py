from typing import Any, Self


contents = {}

class ReducedObject(object):
    """
    Implements parts of builtins.object in a PenguinMod-compatible way.
    """

    # Dervied Builtins Description
    id: int
    #__doc__: str | None
    #__dict__: dict[str, Any]
    #__module__: str
    #__annotations__: dict[str, Any]
    #@property
    #def __class__(self) -> type[Self]: ...
    #@__class__.setter
    #def __class__(self, type: type[Self], /) -> None: ...
    #def __init__(self) -> None: ...
    def __new__(cls) -> Self:
        obj = super.__new__()
        obj.id = len(contents)
        contents[obj.id] = dict()
        return obj

    ## N.B. `object.__setattr__` and `object.__delattr__` are heavily special-cased by type checkers.
    ## Overriding them in subclasses has different semantics, even if the override has an identical signature.
    def __setattr__(self, name: str, value: Any, /) -> None:
        contents[self.id][name] = value
    def __delattr__(self, name: str, /) -> None:
        del contents[self.id][name]
    #def __eq__(self, value: object, /) -> bool: ...
    #def __ne__(self, value: object, /) -> bool: ...
    #def __str__(self) -> str: ...  # noqa: Y029
    #def __repr__(self) -> str: ...  # noqa: Y029
    #def __hash__(self) -> int: ...
    #def __format__(self, format_spec: str, /) -> str: ...
    #def __getattribute__(self, name: str, /) -> Any: ...
    def __getattr__(self, name: str, /) -> Any:
        if name in contents[self.id]:
            return contents[self.id]
        else:
            # Raise using trick:
            super().__getattribute__(self, name)
            raise AttributeError() # In case it works
    #def __sizeof__(self) -> int: ...
    ## return type of pickle methods is rather hard to express in the current type system
    ## see #6661 and https://docs.python.org/3/library/pickle.html#object.__reduce__
    #def __reduce__(self) -> str | tuple[Any, ...]: ...
    #def __reduce_ex__(self, protocol: SupportsIndex, /) -> str | tuple[Any, ...]: ...
    #def __getstate__(self) -> object: ...
    #
    #def __dir__(self) -> Iterable[str]: ...
    #def __init_subclass__(cls) -> None: ...
    #@classmethod
    #def __subclasshook__(cls, subclass: type, /) -> bool: ...

