import logging
import hikari
from hikari.files import Resourceish, Resource, File

import tanjun
from ottbot.core.client import OttClient

component = tanjun.Component()


@component.with_slash_command
@tanjun.as_slash_command("bababooey", "Sends BABABOOEY.MP3")
async def command_bababooey(ctx: tanjun.abc.SlashContext) -> None:
    f = File("ottbot/data/static/BABABOOEY.mp3")
    data = await f.read()
    await ctx.respond(data)


@tanjun.as_loader
def load_component(client: tanjun.Client) -> None:
    client.add_component(component.copy())
