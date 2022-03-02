"""Invite tracker"""

import hikari
import tanjun

from ottbot.core.bot import OttBot
from ottbot.core.db import AsyncPGDatabase
from ottbot.core.utils.funcs import build_loaders, ordinal

component, load_component, unload_component = build_loaders()


invite_group = component.with_slash_command(tanjun.slash_command_group("invite", "Invite related commands"))


@invite_group.with_command
@tanjun.with_member_slash_option("member", "The member to check.", default=None)
@tanjun.as_slash_command("total", "Get the total number of people invited my a member.")
async def cmd_total(
    ctx: tanjun.abc.SlashContext,
    member: hikari.Member | None,
    db: AsyncPGDatabase = tanjun.inject(type=AsyncPGDatabase),
    bot: OttBot = tanjun.inject(type=OttBot),
) -> None:
    if ctx.guild_id is None:
        return

    id = member.id if member else ctx.author.id

    rows = await db.rows("SELECT uses FROM invites WHERE user_id = $1 AND guild_id = $2", id, ctx.guild_id)

    # fields = [()]

    embed = bot.embeds.build(
        ctx,
        title="Invites",
        description=f"{ordinal(len(rows))} people invited by {member.mention if member else ctx.author.mention}",
    )

    print(rows)
    await ctx.respond("...", embed=embed)


@component.with_listener(hikari.MemberCreateEvent)
async def on_member_create(
    event: hikari.MemberCreateEvent, db: AsyncPGDatabase = tanjun.inject(type=AsyncPGDatabase)
) -> None:
    print(f"Member join {event.member.display_name}")
    invites = await event.app.rest.fetch_guild_invites(event.guild_id)
    db_invites: list[tuple[int, str, int]] = await db.rows(
        "SELECT (user_id, code, uses) FROM invites WHERE guild_id = $1", event.guild_id
    )
    sorted_db_invites = sorted(db_invites, key=lambda i: i[1])
    sorted_invites = sorted(invites, key=lambda i: i.code)

    print(sorted_db_invites)
    print(sorted_invites)

    db_ptr = sorted_db_invites.pop()
    invite_ptr = sorted_invites.pop()

    user = None
    code = None
    uses = None

    while sorted_db_invites or sorted_invites:
        print(f"{db_ptr[1]=}")
        print(f"{invite_ptr.code=}")
        if db_ptr[1] == invite_ptr.code:
            if db_ptr[2] != invite_ptr.uses:
                code = invite_ptr.code
                user = invite_ptr.inviter
                uses = invite_ptr.uses
                await db.execute("UPDATE invites SET uses = $1 WHERE code = $2", invite_ptr.uses, code)
                break

        elif db_ptr[1] < invite_ptr.code:
            if sorted_invites:
                invite_ptr = sorted_invites.pop()
            else:
                db_ptr = sorted_db_invites.pop()
        elif db_ptr[1] > invite_ptr.code:
            if sorted_db_invites:
                db_ptr = sorted_db_invites.pop()
            else:
                invite_ptr = sorted_invites.pop()

    if code is not None and user is not None and uses is not None:
        handle_invite_rewards(db, event.guild_id, user, code, uses)

    if user is not None and uses is not None:
        await event.member.send(
            f"You are the {ordinal(uses)} invited to the server by {user.username} with the code {code}"
        )


@component.with_listener(hikari.InviteCreateEvent)
async def on_invite_create(event: hikari.InviteCreateEvent, db: AsyncPGDatabase = tanjun.inject(type=AsyncPGDatabase)):
    print("Invite create event")
    if event.invite.inviter:
        await db.execute(
            "INSERT INTO invites (user_id, guild_id, code, uses, expires_at) VALUES ($1, $2, $3, $4, $5)",
            event.invite.inviter.id,
            event.guild_id,
            event.invite.code,
            event.invite.uses,
            event.invite.expires_at.replace(tzinfo=None) if event.invite.expires_at else None,
        )


def handle_invite_rewards(db: AsyncPGDatabase, guild_id: int, user: hikari.User, code: str, uses: int):
    """Handle and rewards given to users for inviting people defined in a Guild's config"""
    # TODO: ^
    ...


# TODO: add embeds to messages
# ┊ ┊ ┊ ┊⚡ ...
# ┊ ┊ ┊⚡ ...
# ┊ ┊⚡ ...
# ┊⚡ ...
# ⚡ ...
# ➤ ...
# ➤ ...
# ➤ ...

# TODO: subtract total invites when someone leaves
# TODO: Detect new accounts
# TODO: impl handle_invite_rewards

# TODO: getters / setters for db values
# TODO: blacklist for user id -> auto black list for banned users
