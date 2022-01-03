import time
import typing as t
from datetime import timedelta
from platform import python_version

import distro
import hikari
import tanjun
from psutil import Process, virtual_memory

from ottbot.core.bot import OttBot
from ottbot.core.utils.funcs import build_loaders

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
            f"```{len([_ async for _ in bot.rest.fetch_members(ctx.guild_id)] if ctx.guild_id else []):, }```",
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
        ),
    )
