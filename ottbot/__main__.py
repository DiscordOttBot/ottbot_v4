import os

from fastapi import FastAPI
import uvicorn

from ottbot.core.bot import OttBot
from ottbot import __version__

if os.name != "nt":
    import uvloop

    uvloop.install()

app = FastAPI()
bot: OttBot = OttBot(version=__version__)


@app.on_event("startup")
async def api_startup():
    await bot.start()


@app.on_event("shutdown")
async def api_shutdown():
    await bot.close()


uvicorn.run(app=app, host="127.0.0.1", port=8001, log_level="debug")
