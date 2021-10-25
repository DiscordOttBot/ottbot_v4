import os

from fastapi import FastAPI
import uvicorn

from ottbot.core.bot import OttBot
from ottbot import __version__

from ottbot.api.api_factory import APIFactory
from ottbot.api.routers import user, guild

if os.name != "nt":
    import uvloop

    uvloop.install()

app: FastAPI = FastAPI()
bot: OttBot = OttBot(version=__version__)

APIFactory.build(bot, app, [user.router, guild.router])


@app.on_event("startup")
async def api_startup() -> None:
    await bot.start()


@app.on_event("shutdown")
async def api_shutdown() -> None:
    await bot.close()


uvicorn.run(app=app, host="127.0.0.1", port=8001, log_level="debug")
