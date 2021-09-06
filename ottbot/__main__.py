import os

from ottbot.core.bot import OttBot

if os.name != "nt":
    import uvloop

    uvloop.install()

if __name__ == "__main__":
    bot: OttBot = OttBot()
    bot.run()