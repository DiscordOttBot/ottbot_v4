import os
import sys

import hikari
import uvicorn
from fastapi import FastAPI

from ottbot import __version__, log_level
from ottbot.api.api_factory import APIFactory
from ottbot.api.api_wrapper import APIWrapper
from ottbot.api.routers import guild, user
from ottbot.core.bot import OttBot

if os.name != "nt":
    import uvloop

    uvloop.install()


def api_main() -> None:
    """Main entry point for running the bot and it's ReST API"""
    bot: OttBot = OttBot(version=__version__, log_level=log_level)
    app: FastAPI = APIWrapper([user.router, guild.router])

    APIFactory.build(bot, app, [user.router, guild.router])

    @app.on_event("startup")
    async def api_startup() -> None:
        await bot.start_()

    @app.on_event("shutdown")
    async def api_shutdown() -> None:
        await bot.close()

    uvicorn.run(app, host="localhost", port=8001, log_level=log_level)


def bot_main() -> None:
    """Main entry point for only running the bot"""
    bot = OttBot(version=__version__, log_level=log_level)

    bot.run_()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        api_main()
    else:
        bot_main()
