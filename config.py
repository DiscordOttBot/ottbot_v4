from __future__ import annotations
import typing as t
from os import environ
from pathlib import Path
import json

import dotenv

T = t.TypeVar("T")

dotenv.load_dotenv()


class ConfigMeta(type):
    def resolve_value(cls, value: str) -> t.Callable[..., t.Any] | t.Any:

        print(f"[resolve_value] {value}")
        _map: dict[str, t.Callable[..., t.Any]] = {
            "bool": bool,
            "int": int,
            "float": float,
            "str": str,
            "dict": lambda x: json.loads(x),
            "set": lambda x: set([cls.resolve_value(e.strip()) for e in x.split(",")]),
            "file": lambda x: Path(x).read_text().strip("\n"),
            "json": lambda x: json.loads(Path(x).read_text()),
        }

        return _map[(v := value.split(":", maxsplit=1))[0]](v[1])

    def resolve_key(cls, key: str) -> t.Callable[..., t.Any]:
        print(f"[resolve_key] {key}")
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
        print(f"[__getitem__] {name}")
        match name:
            case (var, cast):
                return t.cast(T, cast(cls.resolve_key(var)))

            case (var, set, cast):

                return t.cast(set[T], {cast(v) for v in cls.resolve_key(var)})

            case _:
                return cls.resolve_key(name)


class Config(metaclass=ConfigMeta):
    pass


if t.TYPE_CHECKING:
    reveal_type(Config["DB_PORT"])
    reveal_type(Config["DB_PORT", int])
    reveal_type(Config["OWNER_IDS", set, int])
