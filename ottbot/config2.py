import os
import pathlib
import typing as t

import dotenv

dotenv.load_dotenv()

T = t.TypeVar("T")

class ConfigMeta(type):
    def __getitem__(cls, tup: tuple[str, T]) -> T:
        name, typ = cls._parse_tuple(tup)
        return typ(cls._parse_env_var(os.environ[name], typ))

    def __getattr__(cls, name):
        return cls.__getitem__(name)

    def _parse_tuple(cls, tup) -> tuple[str, t.Callable[[t.Any], T]]:
        if len(tup) == 1:
            return (tup[0], str)
        else:
            return (tup[0], tup[1])

    def _parse_env_var(cls, value, typ: t.Callable[[t.Any], T]) -> T:
        _types: dict[str, t.Callable[..., t.Any]] = {
            "bool": bool,
            "int": int,
            "float": float,
            "file": lambda x: pathlib.Path(x).read_text().strip("\n"),
            "str": str,
            "set": lambda x: set([cls._resolve_value(e.strip()) for e in x.split(",")]),
        }
        return _types[(v := value.split(":", maxsplit=1))[0]](v[1])


class Config(metaclass=ConfigMeta):
    """Second config class"""


print(Config["DB_PORT", int])
print(type(Config["DB_PORT", int]))
