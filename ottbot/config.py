from __future__ import annotations

import traceback
import typing as t
from os import environ
from pathlib import Path

import dotenv

dotenv.load_dotenv()


class ConfigMeta(type):
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
            "file": lambda x: Path(x).read_text().strip("\n"),
            "str": str,
            "set": lambda x: set([cls._resolve_value(e.strip()) for e in x.split(",")]),
        }
        return _types[(v := value.split(":", maxsplit=1))[0]](v[1])

    def _resolve_key(cls, key: str) -> t.Callable[..., t.Any]:
        """Reads environment variable from machine or .env file. In case of type casting, it will call cls._resolve_value(key)"""
        try:
            return cls._resolve_key(environ[key])
        except Exception:  # value contains ":" and needs to be type casted
            return cls._resolve_value(key)

    def __getattr__(cls, name: str):
        try:
            return cls._resolve_key(name)
        except KeyError:
            traceback.print_exc()
            raise AttributeError(f"{name} is not a key in config.") from None

    def __getitem__(cls, name: str):
        return cls.__getattr__(name)


class Config(metaclass=ConfigMeta):
    """Class for accessing environment variables on the machine or .env file.
    Examples:
    `Config.TOKEN`
    `Config["TOKEN"]`
    """

    pass
