import os
import sys

import uvicorn
from fastapi import FastAPI

from ottbot import __version__
from ottbot.api.api_factory import APIFactory
from ottbot.api.routers import guild, user
from ottbot.core.bot import OttBot

if os.name != "nt":
    import uvloop

    uvloop.install()


def api_main() -> None:
    """Main entry point for running the bot and it's ReST API"""
    app: FastAPI = FastAPI()
    bot: OttBot = OttBot(version=__version__)

    APIFactory.build(bot, app, [user.router, guild.router])

    @app.on_event("startup")
    async def api_startup() -> None:
        await bot.start_()

    @app.on_event("shutdown")
    async def api_shutdown() -> None:
        await bot.close()

    uvicorn.run(app=app, host="127.0.0.1", port=8001, log_level="debug")


def main() -> None:
    """Main entry point for only running the bot"""
    bot = OttBot(version=__version__)
    bot.run()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        api_main()
    else:
        main()
