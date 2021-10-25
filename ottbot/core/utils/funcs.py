import glob
import pathlib
import typing as t

import tanjun


def to_dict(obj) -> dict[str, str]:
    """Converts a non-serializable object to a dictionary.

    This function converts all non-private (methods not starting with a `_`)
    to dictonary entries where the attribute name is the key and the attribute
    as a string is the value."""
    d: dict[str, str] = dict()
    for attr in dir(obj):
        if not attr.startswith("_"):
            attribute: t.Any = getattr(obj, attr)
            d[attr] = f"{attribute}"

    return d


# lambda obj: {attr: f"{getattr(obj, attr)}" for attr in dir(obj) if not attr.startswith("_")}


def gen_load_component(component):
    @tanjun.as_loader
    def load_component(client: tanjun.Client) -> None:
        client.add_component(component.copy())

    return load_component()


def load_modules_from_path(path: str, client: tanjun.Client):
    print(path)
    filenames = glob.glob(path + "/**/*.py", recursive=True)
    print(filenames)
    filenames = [f for f in filenames if not f.startswith(("_"))]
    return filenames
    # client.load_modules()
