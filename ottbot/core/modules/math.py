import os
import subprocess

import tanjun

from ottbot.constants import ZWJ
from ottbot.core.bot import OttBot
from ottbot.core.utils.funcs import build_loaders

component, load_component, unload_component = build_loaders()


def generate_image(bot: OttBot, latex: str, name: str, resolution: str):

    latex_file = name + ".tex"
    dvi_file = name + ".dvi"
    png_file = name + "1.png"

    with open(f"{bot._static}/template.tex", "r") as textemplatefile:
        textemplate = textemplatefile.read()

        with open(os.path.join(bot._dynamic, latex_file), "w") as tex:
            backgroundcolour = "36393E"  # discord background colour
            textcolour = "DBDBDB"  # whiteish color
            latex = (
                textemplate.replace("__DATA__", latex)
                .replace("__BGCOLOUR__", backgroundcolour)
                .replace("__TEXTCOLOUR__", textcolour)
            )

            tex.write(latex)
            tex.flush()
            tex.close()
    RES_TO_DPI = {"low": "200", "medium": "1000", "high": "2000"}
    latexsuccess = subprocess.run(
        ["latex", "-no-shell-escape", "-interaction=nonstopmode", latex_file], cwd=bot._dynamic, stdout=subprocess.PIPE
    )
    if latexsuccess.returncode == 0:
        subprocess.run(["dvipng", "-q*", "-D", RES_TO_DPI[resolution], "-T", "tight", dvi_file], cwd=bot._dynamic)
        return png_file
    else:
        return ""


@component.with_slash_command
@tanjun.with_str_slash_option(
    "resolution", "The resolution to generate the image in", choices=["low", "medium", "high"], default="low"
)
@tanjun.with_str_slash_option("expression", "The expression to generate latex from")
@tanjun.as_slash_command("latex", "Generate latex based on an expression")
async def cmd_latex(
    ctx: tanjun.abc.SlashContext, expression: str, resolution: str, bot: OttBot = tanjun.inject(type=OttBot)
) -> None:
    path = generate_image(bot, expression, f"{ctx.author.id}", resolution)
    if path:
        msg = await ctx.respond(ZWJ, ensure_result=True)
        await msg.edit(attachment=f"{bot._dynamic}/{path}")
        bot.clean_dynamic_dir()
    else:
        await ctx.respond("Error creating latex file")
