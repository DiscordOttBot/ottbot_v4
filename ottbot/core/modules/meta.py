import datetime
import time
import typing as t
from datetime import timedelta
from platform import python_version

import hikari
from hikari import permissions

import distro
import tanjun
from ottbot.constants import ZWJ
from ottbot.core.bot import OttBot
from ottbot.core.utils.funcs import build_loaders, ordinal, strfdelta
from psutil import Process, virtual_memory

component, load_component, unload_component = build_loaders()


@component.with_slash_command
@tanjun.as_slash_command("ping", "Ping the bot to check if it's online")
async def cmd_ping(ctx: tanjun.abc.SlashContext, bot: OttBot = tanjun.injected(type=OttBot)) -> None:
    before = time.time()
    msg = await ctx.respond("Pong!", ensure_result=True)
    after = time.time()

    await msg.edit(
        f"{msg.content}\n**Gateway**: {bot.heartbeat_latency * 1000:,.0f} ms\n**REST**: {(after - before) * 1000:,.0f} ms",
    )


@component.with_slash_command
@tanjun.as_slash_command("stats", "Display stats about the bot")
async def cmd_stats(ctx: tanjun.abc.SlashContext, bot: OttBot = tanjun.injected(type=OttBot)):
    bot.lines.count()
    proc = Process()
    with proc.oneshot():
        uptime = timedelta(seconds=time.time() - proc.create_time())
        cpu_time = str(timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user))
        mem_total = virtual_memory().total / (1024 ** 2)
        mem_of_total = proc.memory_percent()
        mem_usage = mem_total * (mem_of_total / 100)

    code_p, docs_p, blank_p = bot.lines.grab_percents()

    fields: t.Optional[list[tuple[str | int, str | int, bool]]] = [
        ("OttBot", f"```{bot.version}```", True),
        ("Python", f"```{python_version()}```", True),
        ("Hikari", f"```{hikari.__version__}```", True),
        (
            "Users here",
            f"```{len([_ async for _ in bot.rest.fetch_members(ctx.guild_id)] if ctx.guild_id else [])}```",
            True,
        ),
        ("Total users", f"```{len(bot.cache.get_users_view()):,}```", True),
        ("Servers", f"```{len(bot.guilds):,}```", True),
        ("Lines of code", f"```{bot.lines.total:,}```", True),
        ("Latency", f"```{bot.heartbeat_latency * 1000:,.0f} ms```", True),
        ("Platform", f"```{distro.name()} {distro.version()}```", True),
        (
            "Code breakdown",
            f"```| {code_p:>5.2f}% | code lines  -> {bot.lines.code:>6} |\n"
            + f"| {docs_p:>5.2f}% | docstrings  -> {bot.lines.docs:>6} |\n"
            + f"| {blank_p:>5.2f}% | blank lines -> {bot.lines.blank:>6} |\n```",
            False,
        ),
        (
            "Files by language",
            f"```| {len(bot.lines.py) / len(bot.lines) * 100:>5.2f}% | .py files   -> {len(bot.lines.py):>6} |\n"
            + f"| {len(bot.lines.sql) / len(bot.lines) * 100:>5.2f}% | .sql files  -> {len(bot.lines.sql):>6} |```",
            False,
        ),
        (
            "Memory usage",
            f"```| {mem_of_total:>5,.2f}% | {mem_usage:,.0f} MiB  /  {(mem_total):,.0f} MiB |```",
            False,
        ),
        ("Uptime", f"```{str(uptime)[:-4]}```", True),
        ("CPU time", f"```{cpu_time[:-4]}```", True),
        (
            "Database calls since uptime",
            f"```{bot.pool.calls:,} ({bot.pool.calls / (uptime.total_seconds() / 60):,.6f}" + " / minute)```",
            False,
        ),
    ]
    await ctx.respond(
        embed=bot.embeds.build(
            ctx=ctx,
            header=" ",
            title="System stats",
            thumbnail=me.avatar_url if (me := bot.get_me()) is not None else "None",
            fields=fields,
            # color=me.get_me().accent_color
        ),
    )


@component.with_slash_command
@tanjun.with_member_slash_option("user", "The user to get infomation about", default=None)
@tanjun.as_slash_command("user_info", "Information about a user")
async def cmd_user_info(
    ctx: tanjun.abc.SlashContext, user: hikari.Member | None, bot: OttBot = tanjun.injected(type=OttBot)
) -> None:
    if user is None:
        user = await bot.rest.fetch_member(ctx.guild_id, ctx.author)

    guild = await ctx.fetch_guild()
    user_roles = await user.fetch_roles()
    guild_roles = await bot.rest.fetch_roles(ctx.guild_id)

    presence = user.get_presence()
    top_role = user.get_top_role()
    permissions = tanjun.utilities.calculate_permissions(user, guild, {role.id: role for role in user_roles})

    administrator = (permissions & hikari.Permissions.ADMINISTRATOR) == hikari.Permissions.ADMINISTRATOR

    existed_for = strfdelta(datetime.datetime.now(tz=datetime.timezone.utc) - user.created_at, "{D}d, {H}h, {M}m, {S}s")
    member_for = strfdelta(datetime.datetime.now(tz=datetime.timezone.utc) - user.joined_at, "{D}d, {H}h, {M}m, {S}s")
    booster_for = (
        strfdelta(datetime.datetime.now(tz=datetime.timezone.utc) - user.premium_since, "{D}d, {H}h, {M}m, {S}s")
        if user.premium_since
        else ZWJ
    )

    fields = [
        ("ID", user.id, False),
        ("Descriminator", user.discriminator, True),
        ("Bot?", user.is_bot, True),
        ("Admin?", administrator, True),
        ("Created on", f"<t:{user.created_at.timestamp():.0f}:f>", True),
        ("Joined on", f"<t:{user.joined_at.timestamp():.0f}:f>", True),
        ("Boosted on", f"<t:{user.premium_since.timestamp():.0f}:f>" if user.premium_since else ZWJ, True),
        ("Existed for", existed_for, True),
        ("Member for", member_for, True),
        ("Booster for", booster_for, True),
        ("Status", presence.visible_status.title() if presence is not None else "Offline", True),
        (
            "Activity type",
            str(presence.activities[-1].type).title()
            if hasattr(presence, "activities")
            else presence
            if presence is not None
            else ZWJ,
            True,
        ),
        (
            "Activity name",
            presence.activities[-1].name.title()
            if hasattr(presence, "activities")
            else presence
            if presence is not None
            else ZWJ,
            True,
        ),
        ("Nº of roles", len(user_roles) - 1, True),
        ("Top role", f"{top_role.mention} | ID: {top_role.id}", True),
        ("Top role position", f"{ordinal(len(guild_roles) - top_role.position)} / {len(guild_roles):,}", True),
    ]
    embed = bot.embeds.build(
        ctx=ctx,
        title="User Information",
        description=f"Information about {user.mention}",
        fields=fields,
    )

    await ctx.respond(embed=embed)


@component.with_slash_command
@tanjun.as_slash_command("server_info", "Information about the current server information")
async def cmd_server_info(ctx: tanjun.abc.SlashContext, bot: OttBot = tanjun.injected(type=OttBot)) -> None:
    guild = await ctx.fetch_guild()
    guild_roles = await guild.fetch_roles()
    guild_members = guild.get_members()
    guild_channels = guild.get_channels()

    text_channels = {id: g for id, g in guild_channels.items() if g.type == hikari.ChannelType.GUILD_TEXT}
    voice_channels = {id: g for id, g in guild_channels.items() if g.type == hikari.ChannelType.GUILD_VOICE}

    humans = [guild_members[id] for id in guild_members.keys() if not guild_members[id].is_bot]
    bots = [guild_members[id] for id in guild_members.keys() if guild_members[id].is_bot]

    GUILD_LEVEL_TO_MAX_EMOJIS = {0: 50, 1: 100, 2: 150, 3: 250}

    fields = [
        ("ID", ctx.guild_id, False),
        ("Owner", f"<@{guild.owner_id}>", False),
        ("Top role", sorted(guild_roles, key=lambda r: r.position)[-1].mention, True),
        ("Members", f"{len(guild_members):,}", True),
        ("Humans / bots", f"{len(humans):,} / {len(bots):,}", True),
        (
            "Bans",
            f"{len(bans):,}" if (bans := await bot.rest.fetch_bans(guild)) else "-",
            True,
        ),
        ("Roles", f"{len(guild_roles)-1:,}", True),
        ("Text channels", f"{len(text_channels):,}", True),
        ("Voice channels", f"{len(voice_channels):,}", True),
        (
            "Invites",
            f"{len(await bot.rest.fetch_guild_invites(guild)):,}",
            True,
        ),
        ("Emojis", f"{len(guild.get_emojis()):,} / {GUILD_LEVEL_TO_MAX_EMOJIS[int(guild.premium_tier)]:,}", True),
        ("Boosts", f"{guild.premium_subscription_count:,} (level {int(guild.premium_tier)})", True),
        ("Newest member", max((m for _, m in guild_members.items()), key=lambda m: m.joined_at).mention, True),
        ("Created on", f"<t:{guild.created_at.timestamp():.0f}:D>", True),
        (
            "Existed for",
            strfdelta(datetime.datetime.now(tz=datetime.timezone.utc) - guild.created_at, "{D}d, {H}h, {M}m, {S}s"),
            True,
        ),
        (
            "Statuses",
            (
                f"🟢 {len([m for _, m in guild_members.items() if isinstance(m, hikari.Member) and m.get_presence() and m.get_presence().visible_status == hikari.Status.ONLINE]):,} "
                f"🟠 {len([m for _, m in guild_members.items() if isinstance(m, hikari.Member) and m.get_presence() and m.get_presence().visible_status == hikari.Status.IDLE]):,} "
                f"🔴 {len([m for _, m in guild_members.items() if isinstance(m, hikari.Member) and m.get_presence() and m.get_presence().visible_status == hikari.Status.DO_NOT_DISTURB]):,} "
                f"⚪ {len([m for _, m in guild_members.items() if isinstance(m, hikari.Member) and m.get_presence() is None]):,}"
            ),
            False,
        ),
    ]
    [print(m.get_presence()) for _, m in guild_members.items() if isinstance(m, hikari.Member)]
    embed = bot.embeds.build(
        ctx=ctx,
        title="Server Information",
        description=f"Information about **{guild.name}**",
        fields=fields,
        header_icon=guild.icon_url,
    )

    await ctx.respond(embed=embed)

    # TODO: Channel/Catagory Info
    # TODO: Role Info
    # TODO: Message Info
    # TODO: Paginator -> detailed server info
