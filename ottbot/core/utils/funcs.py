import asyncio
import collections.abc as collections_abc
import functools
import glob
import logging
import os
import pathlib
import typing as t
from string import Formatter

import hikari
import tanjun
import yuyo

from ottbot import constants


def to_dict(obj, ignore_underscores: bool = True) -> dict[str, str]:
    """
    Converts a non-serializable object to a dictionary.

    This function converts all non-private (methods not starting with a `_`)
    to dictionary entries where the attribute name is the key and the attribute
    as a string is the value.
    """
    d: dict[str, str] = dict()
    for attr in dir(obj):
        if not attr.startswith("_") or not ignore_underscores:
            attribute: t.Any = getattr(obj, attr)
            d[attr] = f"{attribute}"

    return d


# lambda obj: {attr: f"{getattr(obj, attr)}" for attr in dir(obj) if not attr.startswith("_")}


def build_loaders(
    checks: list = [],
) -> tuple[tanjun.Component, t.Callable[[tanjun.Client], None], t.Callable[[tanjun.Client], None]]:
    """
    Creates function that load and unload a component.

    Args:
        component (tanjun.Component): The component to load and unload.

    Returns:
        tuple(Callable[[tanjun.Client], None], Callable[[tanjun.Client], None]):
            A tuple of functions that load and unload the component respectively.
    """
    component = tanjun.Component()
    if checks:
        for check in checks:
            component.add_check(check)

    @tanjun.as_loader
    def load_component(client: tanjun.Client) -> None:
        client.add_component(component.copy())

    @tanjun.as_unloader
    def unload_component(client: tanjun.Client) -> None:
        client.remove_component_by_name(component.name)

    return (component, load_component, unload_component)


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


def get_list_of_files(dir_name: str, ignore_underscores: bool = True) -> list[pathlib.Path]:
    """
    Returns the partial path separated by '.'s of all the .py
    files in a given directory where the root is given directory.

    Args:
        dir_name (str): The directory to search in.
        ignore_underscores (bool): Whether to ignore files that start
            with an underscore.
    """

    list_of_files = os.listdir(dir_name)
    all_files = list()
    # Iterate over all the entries
    for entry in list_of_files:
        # Create full path
        full_path = os.path.join(dir_name, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            all_files += get_list_of_files(full_path)
        else:
            if full_path.endswith(".py"):
                if ignore_underscores and full_path.split(os.sep)[-1].startswith("_"):
                    continue
                else:
                    all_files.append(pathlib.Path(full_path))

    return all_files


def type_check(func):
    @functools.wraps(func)
    def check(*args, **kwargs):
        for i in range(len(args)):
            v = args[i]
            v_name = list(func.__annotations__.keys())[i]
            v_type = list(func.__annotations__.values())[i]
            error_msg = "Variable `" + str(v_name) + "` should be type ("
            error_msg += str(v_type) + ") but instead is type (" + str(type(v)) + ")"
            if not isinstance(v, v_type):
                raise TypeError(error_msg)

        result = func(*args, **kwargs)
        v = result
        v_name = "return"
        v_type = func.__annotations__["return"]
        error_msg = "Variable `" + str(v_name) + "` should be type ("
        error_msg += str(v_type) + ") but instead is type (" + str(type(v)) + ")"
        if not isinstance(v, v_type):
            raise TypeError(error_msg)
        return result

    return check


async def delete_button_callback(ctx: yuyo.ComponentContext) -> None:
    author_ids = set(
        map(hikari.Snowflake, ctx.interaction.custom_id.removeprefix(constants.DELETE_CUSTOM_ID).split(","))
    )
    if (
        ctx.interaction.user.id in author_ids
        or ctx.interaction.member
        and author_ids.intersection(ctx.interaction.member.role_ids)
    ):
        await ctx.defer(hikari.ResponseType.DEFERRED_MESSAGE_UPDATE)
        await ctx.delete_initial_response()

    else:
        await ctx.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE, "You do not own this message", flags=hikari.MessageFlag.EPHEMERAL
        )


async def collect_response(  # pylint: disable=too-many-branches
    ctx: tanjun.abc.SlashContext,
    validator: list[str] | collections_abc.Callable | None = None,
    timeout: int = 60,
    timeout_msg: str = "Waited for 60 seconds... Timeout.",
) -> hikari.GuildMessageCreateEvent | None:
    """
    Helper function to collect a user response.

    Parameters
    ==========
    ctx: SlashContext
        The context to use.
    validator: list[str] | Callable | None = None
        A validator to check against. Validators can be:
            - list - A list of strings to match against.
            - Callable/Function - A function accepting (ctx, event) and returning bool.
            - None - Skips validation and returns True always.
    timeout int = 60
        The default wait_for timeout to use.
    timeout_msg: str = Waited for 60 seconds ... Timeout.
        The message to display if a timeout occurs
    """

    def is_author(event: hikari.GuildMessageCreateEvent) -> bool:
        return ctx.author == event.message.author

    # is_author: collections_abc.Callable[[hikari.GuildMessageCreateEvent], bool] = (
    #     lambda event: ctx.author == event.message.author
    # )

    while True:
        try:
            if ctx.client.events is not None:
                event = await ctx.client.events.wait_for(
                    hikari.GuildMessageCreateEvent, predicate=is_author, timeout=timeout
                )
            else:
                return None
        except asyncio.TimeoutError:
            await ctx.edit_initial_response(timeout_msg)
            return None

        if event is None or event.content is None:
            return None

        if event.content == "❌":
            return None

        if not validator:  # exit if there are no extra checks to be run
            return event

        if isinstance(validator, list):
            if any(valid_resp.lower() == event.content.lower() for valid_resp in validator):
                return event
            validation_message = await ctx.respond(
                f"That wasn't a valid response... Expected one these: {' - '.join(validator)}", ensure_result=True
            )
            await asyncio.sleep(3)
            await validation_message.delete()

        elif asyncio.iscoroutinefunction(validator):
            valid = await validator(ctx, event)
            if valid:
                return event
            validation_message = await ctx.respond(
                "That doesn't look like a valid response... Try again?", ensure_result=True
            )
            await asyncio.sleep(3)
            await validation_message.delete()

        elif callable(validator):
            if validator(ctx, event):
                return event
            validation_message = await ctx.respond(
                "Something about that doesn't look right... Try again?", ensure_result=True
            )
            await asyncio.sleep(3)
            await validation_message.delete()


async def ensure_guild_channel_validator(ctx: tanjun.abc.Context, event: hikari.GuildMessageCreateEvent) -> bool:
    """
    Used as a validator for `collect_response` to ensure a text channel in a guild exists.
    """
    guild = ctx.get_guild()
    if not guild:
        return False
    channels = guild.get_channels() if guild else []
    found_channel = None

    for channel_id in channels:
        channel = guild.get_channel(channel_id)
        if channel is None or event.content is None:
            continue
        if str(channel.id) in event.content or channel.name == event.content:
            found_channel = channel
            break

    if found_channel:
        return True

    await ctx.edit_initial_response(content=f"Channel `{event.content}` not found! Try again?")
    await event.message.delete()
    await asyncio.sleep(5)
    return False


def is_int_validator(_, event: hikari.GuildMessageCreateEvent) -> bool:
    """
    Used as a validator for `collect_response` to ensure the message content is an integer.
    """
    try:
        if event.content:
            int(event.content)
            return True
    except ValueError:
        pass
    return False


# Async lambdas for laters
# key=lambda x: (await somefunction(x) for _ in '_').__anext__()
# def head(async_iterator): return async_iterator.__anext__()

# key=lambda x: head(await somefunction(x) for _ in '_')


def strfdelta(tdelta, fmt="{D:02}d {H:02}h {M:02}m {S:02}s", inputtype="timedelta"):
    """Convert a datetime.timedelta object or a regular number to a custom-
    formatted string, just like the stftime() method does for datetime.datetime
    objects.

    The fmt argument allows custom formatting to be specified.  Fields can
    include seconds, minutes, hours, days, and weeks.  Each field is optional.

    Some examples:
        '{D:02}d {H:02}h {M:02}m {S:02}s' --> '05d 08h 04m 02s' (default)
        '{W}w {D}d {H}:{M:02}:{S:02}'     --> '4w 5d 8:04:02'
        '{D:2}d {H:2}:{M:02}:{S:02}'      --> ' 5d  8:04:02'
        '{H}h {S}s'                       --> '72h 800s'

    The inputtype argument allows tdelta to be a regular number instead of the
    default, which is a datetime.timedelta object.  Valid inputtype strings:
        's', 'seconds',
        'm', 'minutes',
        'h', 'hours',
        'd', 'days',
        'w', 'weeks'
    """

    # Convert tdelta to integer seconds.
    if inputtype == "timedelta":
        remainder = int(tdelta.total_seconds())
    elif inputtype in ["s", "seconds"]:
        remainder = int(tdelta)
    elif inputtype in ["m", "minutes"]:
        remainder = int(tdelta) * 60
    elif inputtype in ["h", "hours"]:
        remainder = int(tdelta) * 3600
    elif inputtype in ["d", "days"]:
        remainder = int(tdelta) * 86400
    elif inputtype in ["w", "weeks"]:
        remainder = int(tdelta) * 604800

    f = Formatter()
    desired_fields = [field_tuple[1] for field_tuple in f.parse(fmt)]
    possible_fields = ("W", "D", "H", "M", "S")
    constants = {"W": 604800, "D": 86400, "H": 3600, "M": 60, "S": 1}
    values = {}
    for field in possible_fields:
        if field in desired_fields and field in constants:
            values[field], remainder = divmod(remainder, constants[field])
    return f.format(fmt, **values)


ORDINAL_ENDINGS = {"1": "st", "2": "nd", "3": "rd"}


def ordinal(number):
    if str(number)[-2:] not in ("11", "12", "13"):
        return f"{number:,}{ORDINAL_ENDINGS.get(str(number)[-1], 'th')}"
    else:
        return f"{number:,}th"
