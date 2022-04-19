from __future__ import annotations

import typing
from collections import abc as collections_abc

import hikari
import tanjun
from tanjun import abc as tanjun_abc
from tanjun.checks import _Check
from tanjun.checks import _CommandT as CommandT

from ottbot.config import Config


def is_bot_owner_check(ctx: tanjun.abc.SlashContext) -> bool:
    return int(ctx.author.id) in Config["OWNER_IDS", set, int]


class HasAnyRoleCheck(_Check):
    """Helper class for `with_any_role_check`"""

    __slots__ = ("required_roles",)

    def __init__(
        self,
        roles: collections_abc.Sequence[typing.Union[hikari.SnowflakeishOr[hikari.Role], str]] = [],
        *,
        error_message: typing.Optional[str] = "You do not have the required roles to use this command!",
        halt_execution: bool = True,
    ) -> None:
        super().__init__(error_message, halt_execution)
        self.required_roles = roles

    async def __call__(self, ctx: tanjun_abc.Context, /) -> bool:
        if not ctx.member:
            return self._handle_result(False)

        guild_roles = ctx.cache.get_roles_view_for_guild(ctx.member.guild_id) if ctx.cache else None
        if not guild_roles:
            guild_roles = await ctx.rest.fetch_roles(ctx.member.guild_id)  # type: ignore
            member_roles = [role for role in guild_roles if role.id in ctx.member.role_ids]  # type: ignore
        else:
            member_roles = [guild_roles.get(role) for role in ctx.member.role_ids]

        return self._handle_result(any(map(self._check_roles, member_roles)))

    def _check_roles(self, member_role: typing.Union[int, hikari.Role, None]) -> bool:
        if member_role is None:
            return False
        if isinstance(member_role, int):
            return any(member_role == check for check in self.required_roles)

        return any(member_role.id == check or member_role.name == check for check in self.required_roles)


def with_any_role_check(
    roles: collections_abc.Sequence[typing.Union[hikari.SnowflakeishOr[hikari.Role], int, str]] = [],
    *,
    error_message: typing.Optional[str] = "You do not have the required roles to use this command!",
    halt_execution: bool = False,
) -> collections_abc.Callable[[CommandT], CommandT]:
    """Only let a command run if the author has a specific role and the command is called in a guild.

    Parameters
    ----------
    roles: collections_abc.Sequence[Union[SnowflakeishOr[Role], int, str]]
        The author must have at least one (1) role in this list. (Role.name and Role.id are checked)

    Other Parameters
    ----------------
    error_message: Optional[str]
        The error message raised if the member does not have a required role.

        Defaults to 'You do not have the required roles to use this command!'
    halt_execution: bool
        Whether this check should raise `tanjun.errors.HaltExecution` to
        end the execution search when it fails instead of returning `False`.

        Defaults to `False`.

    Returns
    -------
    collections_abc.abc.Callable[[CommandT], CommandT]
        A command decorator callback which adds the check.
    """
    return lambda command: command.add_check(
        HasAnyRoleCheck(roles, error_message=error_message, halt_execution=halt_execution)
    )
