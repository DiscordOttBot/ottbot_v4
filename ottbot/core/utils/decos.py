# TODO: Update typing when mypy get `ParamSpec` and `Concatenate`
import typing as t
import collections.abc as c

R = t.TypeVar("R")  # return type


def with_ctx(func: c.Callable[..., t.Any]) -> c.Callable[..., t.Any]:
    def wrapper(*args, **kwargs):
        val = func("Ctx", *args, **kwargs)
        return val

    return wrapper


def deco(bot: str, client: str) -> c.Callable[..., c.Callable[..., R]]:
    def inner(func: c.Callable[..., R]) -> c.Callable[..., R]:
        def wrapper(*args: list[t.Any], **kwargs: dict[str, t.Any]) -> R:
            val = func(bot, client, *args, **kwargs)
            return val

        return wrapper

    return inner


@deco("Bot", "Client")
@with_ctx
def add(ctx, bot, client, x, y):
    print(ctx, bot, client)
    return x + y


print(add(1, 2))
