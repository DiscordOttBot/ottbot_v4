import functools
import hikari
from ottbot.core.db.db import AsyncPGDatabase

import tanjun
import yuyo
from ottbot.core.utils.funcs import build_loaders
from ottbot.core.bot import OttBot

component, load_component, unload_component = build_loaders()


async def give_autorole(ctx: yuyo.ComponentContext) -> None:
    if ctx.interaction.member is None:
        return

    guild_id, role_id = [int(x) for x in ctx.interaction.custom_id.split("_")[1:]]

    role = next(filter(lambda r: r.id == role_id, (await ctx.interaction.app.rest.fetch_roles(guild_id))))

    await ctx.interaction.member.add_role(role, reason="Auto-role")
    await ctx.interaction.create_initial_response(
        hikari.ResponseType.MESSAGE_CREATE, f"Gave you {role.mention}", flags=hikari.MessageFlag.EPHEMERAL
    )


@component.with_slash_command
@tanjun.with_role_slash_option("role", "the role to add to autorole")
@tanjun.as_slash_command("autorole", "Automatically assign roles to members.")
async def cmd_autorole(
    ctx: tanjun.abc.SlashContext,
    role: hikari.Role,
    component_client: yuyo.ComponentClient = tanjun.injected(type=yuyo.ComponentClient),
    db: AsyncPGDatabase = tanjun.injected(type=AsyncPGDatabase),
    bot: OttBot = tanjun.injected(type=OttBot),
) -> None:
    if ctx.guild_id is None:
        return

    current = await db.rows("SELECT * FROM auto_roles WHERE guild_id = $1", ctx.guild_id)
    print("current autorole", current)
    if current and (len(current) > 3):
        await ctx.respond("You can only have 3 autoroles per guild.")
        return

    try:
        component_client.set_constant_id(f"autorole_{ctx.guild_id}_{role.id}", functools.partial(give_autorole, bot))
    except ValueError:
        await ctx.respond("That role is already registered")

    await db.execute("INSERT INTO auto_roles (guild_id, role_id) VALUES ($1, $2)", ctx.guild_id, role.id)

    await ctx.respond(f"Added {role.name} to autoroles")


@component.with_slash_command
@tanjun.as_slash_command("autorolemsg", "Send a message with the buttons for autoroles")
async def cmd_autorolemsg(
    ctx: tanjun.abc.SlashContext,
    db: AsyncPGDatabase = tanjun.injected(type=AsyncPGDatabase),
    bot: OttBot = tanjun.injected(type=OttBot),
    cc: yuyo.ComponentClient = tanjun.injected(type=yuyo.ComponentClient),
) -> None:
    if ctx.guild_id is None:
        return
    row = bot.rest.build_action_row()

    role_ids = await db.column("SELECT role_id FROM auto_roles WHERE guild_id = $1", ctx.guild_id)
    for id in role_ids:
        role = bot.cache.get_role(id)
        if role is None:
            role = next(filter(lambda r: r.id == id, await bot.rest.fetch_roles(ctx.guild_id)))

        row.add_button(hikari.ButtonStyle.PRIMARY, f"autorole_{ctx.guild_id}_{role.id}").set_label(
            f"{role.name}"
        ).add_to_container()

    await ctx.respond("Auto Roles", component=row)


@component.with_listener(hikari.StartedEvent)
async def register_auto_role_callbacks(
    event: hikari.StartedEvent,
    component_client: yuyo.ComponentClient = tanjun.injected(type=yuyo.ComponentClient),
    bot: OttBot = tanjun.injected(type=OttBot),
    db: AsyncPGDatabase = tanjun.injected(type=AsyncPGDatabase),
) -> None:

    ids = await db.rows("SELECT (guild_id, role_id) FROM auto_roles")
    if ids:
        for gid, rid in ids:
            component_client.set_constant_id(f"autorole_{gid}_{rid}", give_autorole)
