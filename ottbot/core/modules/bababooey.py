import hikari
from hikari.messages import Attachment

import tanjun
from ottbot.core.client import OttClient

component = tanjun.Component()


@component.with_slash_command
@tanjun.as_slash_command("bababooey", "Sends BABABOOEY.MP3")
async def command_bababooey(ctx: tanjun.abc.MessageContext) -> None:

    await ctx.respond(attachment="../../../data/static/BABABOOEY.mp3")


@tanjun.as_loader
def load_component(client: OttClient) -> None:
    client.add_component(component.copy())
