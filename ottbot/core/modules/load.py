from ottbot.core.utils.checks import is_bot_owner
import tanjun

from ottbot.core.bot import SERVER_ID, OttBot
from ottbot.core.utils.funcs import build_loaders, get_list_of_files

component, load_component, unload_component = build_loaders(checks=[is_bot_owner])


@component.with_slash_command
@tanjun.with_str_slash_option("module", "Module to load", default="")
@tanjun.as_slash_command("load", "Load a module")
async def cmd_load(
    ctx: tanjun.abc.SlashContext,
    module: str,
    bot: OttBot = tanjun.injected(type=OttBot),
) -> None:
    modules = get_list_of_files(module)
    bot.client.load_modules_(module)
    await ctx.respond(f"loaded {[m.stem for m in modules]}")


@component.with_slash_command
@tanjun.with_str_slash_option("module", "Module to unload", default="")
@tanjun.as_slash_command("unload", "Unload a module")
async def cmd_unload(
    ctx: tanjun.abc.SlashContext,
    module: str,
    bot: OttBot = tanjun.injected(type=OttBot),
) -> None:
    modules = get_list_of_files(
        "ottbot/core/modules/" + module, ignore_underscores=False
    )
    for m in modules:
        try:
            bot.client.unload_modules(m)
        except ValueError:  # module isn't loaded
            ...
    await ctx.respond(f"Unloaded modules {[m.stem for m in modules]}")


@component.with_slash_command
@tanjun.with_str_slash_option("module", "Module to update", default="")
@tanjun.as_slash_command("update", "Update slash commands in module(s)")
async def cmd_update(
    ctx: tanjun.abc.SlashContext,
    module: str,
    bot: OttBot = tanjun.injected(type=OttBot),
) -> None:
    modules = get_list_of_files("ottbot/core/modules/" + module)
    for m in modules:
        try:
            bot.client.reload_modules(m)
        except ValueError:
            print(f"\n\nValueError\n{m}\n\n")
            bot.client.load_modules(m)

    await ctx.respond(f"Updated modules {[m.stem for m in modules]}")


@component.with_slash_command
@tanjun.with_str_slash_option("module", "Module to update", default="")
@tanjun.as_slash_command("reload", "Reload slash commands in module(s)")
async def cmd_reload(
    ctx: tanjun.abc.SlashContext,
    module: str,
    bot: OttBot = tanjun.injected(type=OttBot),
) -> None:
    modules = get_list_of_files("ottbot/core/modules/" + module)
    for m in modules:
        try:
            bot.client.reload_modules(m)
        except ValueError:
            print(f"\n\nValueError\n{m}\n\n")
            bot.client.load_modules(m)
    await bot.client.declare_global_commands(guild=SERVER_ID)

    await ctx.respond(f"Reloaded modules {[m.stem for m in modules]}")
