import typing as t


T = t.TypeVar("T")


class MetaFrac(type, t.Generic[T]):
    n: T
    d: T
    def __getitem__(cls, key: str) -> T:
        if key == "n":
            return cls.n
        elif key == "d":
            return cls.d
        elif key == "f":
            return "f"
        else:
            raise KeyError(f"{key} is not a key in {cls.__name__}.")
        
class Frac(metaclass=MetaFrac):
    def __init__(self, n: T, d: T):
        self.n = n
        self.d = d
        
    def __str__(self) -> str:
        return f"{self.n}/{self.d}"
    
reveal_type(Frac["f"])