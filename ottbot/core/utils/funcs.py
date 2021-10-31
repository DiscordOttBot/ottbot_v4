import glob
import logging
import typing as t

import tanjun


def to_dict(obj) -> dict[str, str]:
    """
    Converts a non-serializable object to a dictionary.

    This function converts all non-private (methods not starting with a `_`)
    to dictionary entries where the attribute name is the key and the attribute
    as a string is the value.
    """
    d: dict[str, str] = dict()
    for attr in dir(obj):
        if not attr.startswith("_"):
            attribute: t.Any = getattr(obj, attr)
            d[attr] = f"{attribute}"

    return d


# lambda obj: {attr: f"{getattr(obj, attr)}" for attr in dir(obj) if not attr.startswith("_")}


def build_load_component(component) -> t.Callable[[tanjun.Client], None]:
    """Generates a function that loads a component."""

    @tanjun.as_loader
    def load_component(client: tanjun.Client) -> None:
        client.add_component(component.copy())

    return load_component


def load_modules_from_path(path: str, client: tanjun.Client):
    """Loads all modules from a given path."""

    print(path)
    filenames = glob.glob(path + "/**/*.py", recursive=True)
    print(filenames)
    filenames = [f for f in filenames if not f.startswith(("_"))]
    return filenames
    # client.load_modules()


def parse_log_level(level: t.Union[str, int]) -> int:
    """
    Parses a log level string to an integer.

    This function parses a log level string to an integer. The string can
    either be a number or a string that is a valid log level.

    Args:
        level (str | int): The log level to parse.

    Returns:
        int: The parsed log level.

    Raises:
        ValueError: If the log level is invalid.
    """
    if isinstance(level, int):
        return level
    elif level.isdigit():
        return int(level)
    elif type(level) is str:
        lvl = logging._nameToLevel[level.upper()]
        if lvl is not None:
            return lvl
    raise ValueError(f"Invalid log level: {level}")
