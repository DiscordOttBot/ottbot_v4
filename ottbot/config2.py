import os
import pathlib
import traceback
import typing as t

import dotenv

dotenv.load_dotenv()

T = t.TypeVar("T")


class ConfigMeta(type, t.Generic[T]):
    """Metaclass for extracting environment variables"""

    def _resolve_value(cls, value: str):
        """Type casts values from a string
        Example:
            str:Discord_bot_token -> "Discord_bot_token"
        """
        _types: dict[str, t.Callable[..., t.Any]] = {
            "bool": bool,
            "int": int,
            "float": float,
            "file": lambda x: pathlib.Path(x).read_text().strip("\n"),
            "str": str,
            "set": lambda x: set([cls._resolve_value(e.strip()) for e in x.split(",")]),
        }
        return _types[(v := value.split(":", maxsplit=1))[0]](v[1])

    def _resolve_key(cls, key: str):
        """Reads environment variable from machine or .env file. In case of type casting,
        it will call cls._resolve_value(key)"""
        try:
            return cls._resolve_key(os.environ[key])
        except Exception:  # value contains ":" and needs to be type casted
            return cls._resolve_value(key)

    def __getattr__(cls, name: str):
        try:
            return cls._resolve_key(name)
        except KeyError:
            traceback.print_exc()
            raise AttributeError(f"{name} is not a key in config.") from None

    @t.overload
    def __getitem__(cls, key: str) -> str:
        ...

    @t.overload
    def __getitem__(cls, key: tuple[str, t.Callable[[t.Any], T]]) -> T:
        ...

    @t.overload
    def __getitem__(cls, key: tuple[str, list[t.Callable[[t.Any], T]]]) -> set[T]:
        ...

    def __getitem__(
        cls,
        key: str | tuple[str, t.Callable[[t.Any], T]] | tuple[str, list[t.Callable[[t.Any], T]]],
    ) -> str | T | set[T]:
        if isinstance(key, tuple) and len(key) == 2:  # type specified
            if isinstance(key[1], list):  # type is as set
                # set logic
                print("SET")
                return set()
            return key[1](cls.__getattr__(key[0]))
        elif isinstance(key, str):  # No type specified
            return str(cls.__getattr__(key[0]))
        raise ValueError(
            f"Usage: Config['ENVVAR'], Config['ENVVAR', type], Config['ENVVAR', [type]]. Invalid key: {key!r}"
        )


class Config(metaclass=ConfigMeta):
    """
    Class for accessing environment variables on the machine or .env file.

    Examples:
    `Config.TOKEN`
    `Config["TOKEN"]`
    """

    ...


print(Config["TOKEN", str][10:])
print(Config["DB_PORT", int])
print(Config["OWNER_IDS", [int]])
