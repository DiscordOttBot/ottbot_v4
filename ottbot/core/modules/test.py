import random

import tanjun

from ottbot.core.bot import OttBot

component = tanjun.Component()


@component.with_slash_command
@tanjun.as_slash_command("hello", "Says hello!")
async def command_hello(ctx: tanjun.abc.SlashContext) -> None:
    greeting: str = random.choice(("Hello", "Hi", "Hey"))
    await ctx.respond(
        f"{greeting} {ctx.author.mention if ctx.member else ctx.author.username}!",
        user_mentions=True,
    )


@component.with_slash_command
@tanjun.as_slash_command("test2", "Says hello!")
async def command_test2(ctx: tanjun.abc.SlashContext) -> None:
    greeting: str = random.choice(("Hello", "Hi", "Hey"))
    await ctx.respond(
        f"{greeting} {ctx.author.mention if ctx.member else ctx.author.username}!",
        user_mentions=True,
    )


@component.with_slash_command
@tanjun.with_int_slash_option("number", "The number of dice to roll (max: 25).")
@tanjun.with_int_slash_option(
    "sides", "The number of sides each die will have.", default=6
)
@tanjun.with_int_slash_option(
    "bonus", "A fixed number to add to the total roll.", default=0
)
@tanjun.as_slash_command("dice", "Roll one or more dice.")
async def command_dice(
    ctx: tanjun.abc.SlashContext, number: int, sides: int, bonus: int
) -> None:
    if number > 25:
        await ctx.respond("No more than 25 dice can be rolled at once.")
        return

    if sides > 100:
        await ctx.respond("The dice cannot have more than 100 sides.")
        return

    rolls: list[int] = [random.randint(1, sides) for _ in range(number)]
    await ctx.respond(
        " + ".join(f"{r}" for r in rolls)
        + (f" + {bonus} (bonus)" if bonus else "")
        + f" = **{sum(rolls) + bonus:,}**"
    )


@component.with_slash_command
@tanjun.with_str_slash_option("id_str", "The ID of the user you would like to access")
@tanjun.as_slash_command("user", "Get the name of a user give their ID")
async def cmd_user(
    ctx: tanjun.abc.SlashContext,
    id_str: str,
    bot: OttBot = tanjun.injected(type=OttBot),
) -> None:
    if ctx.guild_id is not None:
        user = bot.cache.get_member(ctx.guild_id, int(id_str))
    if user is not None:
        await ctx.respond(f"{user.mention}")
    else:
        await ctx.respond("User not found")


@tanjun.as_loader
def load_component(client: tanjun.Client) -> None:
    client.add_component(component.copy())
