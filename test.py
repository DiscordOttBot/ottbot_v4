import typing as t
import typing_extensions as te
import collections.abc as c
import logging


T = t.TypeVar("T")
P = te.ParamSpec("P")


def add_logging(f: c.Callable[P, T]) -> c.Callable[P, T]:
    """A type-safe decorator to add logging to a function."""

    def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        logging.info(f"{f.__name__} was called")
        return f(*args, **kwargs)

    return inner


@add_logging
def add_two(x: float, y: float) -> float:
    """Add two numbers together."""
    return x + y


# P = te.ParamSpec("P")
# R = t.TypeVar("R")


# def with_ctx(func: c.Callable[..., t.Any]) -> c.Callable[..., t.Any]:
#     def wrapper(*args, **kwargs):
#         val = func("Ctx", *args, **kwargs)
#         return val

#     return wrapper


# def deco(bot: str, client: str) -> c.Callable[..., c.Callable[..., R]]:
#     def inner(func: c.Callable[..., R]) -> c.Callable[..., R]:
#         def wrapper(*args: list[t.Any], **kwargs: dict[str, t.Any]) -> R:
#             val = func(bot, client, *args, **kwargs)
#             return val

#         return wrapper

#     return inner


# @deco("Bot", "Client")
# @with_ctx
# def add(ctx, bot, client, x, y):
#     print(ctx, bot, client)
#     return x + y


# print(add(1, 2))


# from collections.abc import Callable
# from typing import TypeVar, ParamSpec
