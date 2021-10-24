def to_dict(obj) -> dict:
    d = dict()
    for attr in dir(obj):
        if not attr.startswith("_"):
            attribute = getattr(obj, attr)
            d[attr] = f"{attribute}"

    return d

# print(*[{p: getattr(ctx.author, p)} for p in dir(ctx.author) if not p.startswith("_")])