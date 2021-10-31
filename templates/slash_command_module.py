import tanjun

component = tanjun.Component()

@component.with_slash_command
@tanjun.as_slash_command("example", "An example slash command")
async def cmd_example(ctx: tanjun.abc.SlashContext) -> None:
    await ctx.respond("test")

@tanjun.as_loader
def load_component(client: tanjun.Client) -> None:
    client.add_component(component.copy())