import tanjun


def is_bot_owner(ctx: tanjun.abc.SlashContext) -> bool:
    return ctx.author.id == 425800572671754242
