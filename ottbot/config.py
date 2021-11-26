# type: ignore
# mypy: ignore-errors
"""
This file has been pre-checked with a static type checker, but mypy currently does not support `match case` syntax.
TODO: Remove type: ignore when mypy supports `match case` syntax.
"""
from __future__ import annotations

import builtins
import json
import typing as t
from os import environ
from pathlib import Path

import dotenv

T = t.TypeVar("T")

dotenv.load_dotenv()


class ConfigMeta(type):
    def resolve_value(cls, value: str) -> bool | int | float | str | dict | set[t.Any]:
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

    def resolve_key(cls, key: str) -> bool | int | float | str | dict | set[t.Any]:
        try:
            return cls.resolve_key(environ[key])
        except KeyError:
            return cls.resolve_value(key)

    # def __getattr__(cls, name: str) -> T:
    #     try:
    #         return cls.resolve_key(name)
    #     except KeyError:
    #         raise AttributeError(f"{name} is not a key in config.") from None

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
        key: str | tuple[str, t.Callable[[t.Any], T]] | tuple[str, t.Type[set], t.Callable[[t.Any], T]],
    ) -> str | T | set[T]:
        match key:
            case (var, cast):
                return cast(cls.resolve_key(var))

            case (var, builtins.set, cast):
                if isinstance((resolved := cls.resolve_key(var)), t.Iterable):
                    return {cast(v) for v in resolved}
                raise TypeError(f"{var} is not iterable.")

            case _:
                return str(cls.resolve_key(str(key)))


class Config(metaclass=ConfigMeta):
    pass


# if t.TYPE_CHECKING:
#     reveal_type(Config["DB_PORT"])
#     reveal_type(Config["DB_PORT", int])
#     reveal_type(Config["OWNER_IDS", set, int])
