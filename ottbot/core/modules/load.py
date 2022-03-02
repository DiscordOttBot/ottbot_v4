import tanjun

from ottbot.constants import SERVER_ID
from ottbot.core.client import OttClient
from ottbot.core.utils.checks import is_bot_owner_check
from ottbot.core.utils.funcs import build_loaders, get_list_of_files

component, load_component, unload_component = build_loaders(checks=[is_bot_owner_check])


@component.with_slash_command
@tanjun.with_owner_check()
@tanjun.with_str_slash_option("module", "Module to load", default="")
@tanjun.as_slash_command("load", "Load a module", default_to_ephemeral=True)
async def cmd_load(
    ctx: tanjun.abc.SlashContext,
    module: str,
    client: OttClient = tanjun.inject(type=OttClient),
) -> None:
    modules = get_list_of_files("ottbot/core/modules/" + module)
    client.load_modules_(module)
    await ctx.respond(f"loaded {[m.stem for m in modules]}")


@component.with_slash_command
@tanjun.with_owner_check()
@tanjun.with_str_slash_option("module", "Module to unload", default="")
@tanjun.as_slash_command("unload", "Unload a module", default_to_ephemeral=True)
async def cmd_unload(
    ctx: tanjun.abc.SlashContext,
    module: str,
    client: OttClient = tanjun.inject(type=OttClient),
) -> None:
    modules = get_list_of_files("ottbot/core/modules/" + module, ignore_underscores=False)
    for m in modules:
        try:
            client.unload_modules(m)
        except ValueError:  # module isn't loaded
            ...
    await ctx.respond(f"Unloaded modules {[m.stem for m in modules]}")


@component.with_slash_command
@tanjun.with_owner_check()
@tanjun.with_str_slash_option("module", "Module to update", default="")
@tanjun.as_slash_command("update", "Update slash commands in module(s)", default_to_ephemeral=True)
async def cmd_update(
    ctx: tanjun.abc.SlashContext,
    module: str,
    client: OttClient = tanjun.inject(type=OttClient),
) -> None:
    modules = get_list_of_files("ottbot/core/modules/" + module)
    for m in modules:
        try:
            client.reload_modules(m)
        except ValueError:
            print(f"\n\nValueError\n{m}\n\n")
            client.load_modules(m)

    await ctx.respond(f"Updated modules {[m.stem for m in modules]}")


@component.with_slash_command
@tanjun.with_owner_check()
@tanjun.with_str_slash_option("module", "Module to update", default="")
@tanjun.as_slash_command("reload", "Reload slash commands in module(s)", default_to_ephemeral=True)
async def cmd_reload(
    ctx: tanjun.abc.SlashContext,
    module: str,
    client: OttClient = tanjun.inject(type=OttClient),
) -> None:
    modules = get_list_of_files("ottbot/core/modules/" + module)
    for m in modules:
        try:
            client.reload_modules(m)
        except ValueError:
            print(f"\n\nValueError\n{m}\n\n")
            client.load_modules(m)
    await client.declare_global_commands(guild=SERVER_ID)

    await ctx.respond(f"Reloaded modules {[m.stem for m in modules]}")
