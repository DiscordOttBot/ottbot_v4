import pyqrcode
import tanjun

from ottbot.constants import ZWJ
from ottbot.core.bot import OttBot
from ottbot.core.utils.funcs import build_loaders

component, load_component, unload_component = build_loaders()


@component.with_slash_command
@tanjun.with_str_slash_option("text", "The text to encode")
@tanjun.with_str_slash_option(
    "format", "The format to generate the QR code in", choices=["text", "png", "svg"], default="png"
)
@tanjun.with_int_slash_option("size", "The size of the QR code", default=10)
@tanjun.as_slash_command("qr", "Generate a QR code from the given text.")
async def cmd_qr(
    ctx: tanjun.abc.SlashContext,
    text: str,
    size: int,
    format: str,
    bot: OttBot = tanjun.inject(type=OttBot),
) -> None:
    if size > 100:
        await ctx.respond("Size must be less than 100")
        return
    if len(text) > 1000:
        await ctx.respond("Text must be less than 1000 characters")
        return

    if format == "text":
        code = pyqrcode.create(text).terminal()
        code = code.replace("[49m  [0m", "  ").replace("[7m  [0m", "██")
        code = code.split("\n")[1:-1]
        code = code[4:-4]
        code = [line[8:-8] for line in code]
        code = "\n".join(code)
        await ctx.respond(f"```{code}```")
    elif format == "png":
        code = pyqrcode.create(text)
        code.png(f"{bot._dynamic}/{ ctx.author.id}.png", scale=size, quiet_zone=1)
        msg = await ctx.respond(ZWJ, ensure_result=True)
        await msg.edit(attachment=f"{bot._dynamic}/{ ctx.author.id}.png")
    elif format == "svg":
        code = pyqrcode.create(text)
        code.svg(f"{bot._dynamic}/{ ctx.author.id}.svg", scale=size, quiet_zone=1)
        msg = await ctx.respond(ZWJ, ensure_result=True)
        await msg.edit(attachment=f"{bot._dynamic}/{ ctx.author.id}.svg")
    else:
        await ctx.respond("Invalid format")
    bot.clean_dynamic_dir()


# TODO: Add /code command when discord allows multi line slash commands
# @component.with_slash_command
# @tanjun.with_str_slash_option("language", "The language of the ")
# @tanjun.as_slash_command("code", "Run code")
# async def cmd_code(ctx: tanjun.abc.SlashContext) -> None:
#     await ctx.respond("test")
