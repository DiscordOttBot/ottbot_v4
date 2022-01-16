import tanjun

from ottbot.core.utils.funcs import build_loaders
import yuyo

component, load_component, unload_component = build_loaders()


@component.with_slash_command
@tanjun.as_slash_command("autorole", "Automatically assign roles to members.")
async def cmd_autorole(ctx: tanjun.abc.SlashContext, component_client: yuyo.ComponentClient) -> None:
    if ctx.guild_id is None:
        return

    