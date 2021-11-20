from __future__ import annotations
import typing as t
from os import environ
from pathlib import Path

import dotenv

T = t.TypeVar("T")

dotenv.load_dotenv()


class ConfigMeta(type, t.Generic[T]):
    def resolve_value(cls, value: str) -> t.Callable[..., t.Any] | t.Any:
        _map: dict[str, t.Callable[..., t.Any]] = {
            "bool": bool,
            "int": int,
            "float": float,
            "file": lambda x: Path(x).read_text().strip("\n"),
            "str": str,
            "set": lambda x: set([cls.resolve_value(e.strip()) for e in x.split(",")]),
        }

        return _map[(v := value.split(":", maxsplit=1))[0]](v[1])

    def resolve_key(cls, key: str) -> t.Callable[..., t.Any]:
        try:
            return cls.resolve_key(environ[key])
        except:
            return cls.resolve_value(key)

    def __getattr__(cls, name: str) -> t.Callable[..., t.Any]:
        try:
            return cls.resolve_key(name)
        except KeyError:
            raise AttributeError(f"{name} is not a key in config.") from None

    @t.overload
    def __getitem__(cls, key: str) -> str:
        ...

    @t.overload
    def __getitem__(cls, key: tuple[str, t.Callable[[t.Any], T]]) -> T:
        ...

    @t.overload
    def __getitem__(cls, key: tuple[str, t.Type[set], t.Callable[[t.Any], T]]) -> set[T]:
        ...

    def __getitem__(
        cls,
        name: str | tuple[str, t.Callable[[t.Any], T]] | tuple[str, t.Type[set], t.Callable[[t.Any], T]],
    ) -> str | T | set[T]:
        match name:
            case (var, cast):
                return cast(cls.resolve_key(var))

            case (var, set, cast):
                return {cast(v) for v in cls.resolve_key(var)}
            case _:
                return name


class Config(metaclass=ConfigMeta):
    pass


print((p := Config["DB_PORT"]), type(p))  # DB_PORT=int:5432
print((p := Config["DB_PORT", int]), type(p))  # DB_PORT=int:5432
print((p := Config["OWNER_IDS", set, int]), type(p), type(p.copy().pop()))  # OWNER_IDS=set:int:425800572671754242
