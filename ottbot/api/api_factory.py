from fastapi import FastAPI, APIRouter, HTTPException

from ottbot.core.bot import OttBot




c


class APIFactory(object):
    @staticmethod
    def build(bot: OttBot, app: FastAPI, routers: list[APIRouter]):

        for router in routers:
            app.include_router(router)
            app.bot = bot

            router.app = app
            router.bot = bot


bot = OttBot("OttBot")

app = APIWrapper(data="hello")


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/data")
async def get_data():
    return app.data


item_router = RouterWrapper(prefix="/item", tags=["Items"])


@item_router.get("/")
async def get_items():
    return item_router.bot.db


@item_router.get("/data")
async def item_get_data():
    return item_router.app.data


@item_router.get("/bot")
async def get_bot_items():
    if isinstance(item_router.bot, OttBot):
        return item_router.app.bot.name

    else:
        raise HTTPException(status_code=404, detail="Bot not found")


@item_router.get("/{id_}")
async def get_item(id_: str):
    return "1"
    raise HTTPException(status_code=404, detail=f"Item with id {id_} not found")


APIFactory.build(bot, app, [item_router])
