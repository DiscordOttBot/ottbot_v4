import typing as t


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
