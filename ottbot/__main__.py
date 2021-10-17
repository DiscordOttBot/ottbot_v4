import os

from ottbot.core.bot import OttBot


if os.name != "nt":
    import uvloop

    uvloop.install()

bot: OttBot = OttBot(version="4.0.0a")
bot.run()
