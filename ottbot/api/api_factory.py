from fastapi import APIRouter, FastAPI
from ottbot.core.bot import OttBot


class APIFactory(object):
    @staticmethod
    def build(bot: OttBot, app: FastAPI, routers: list[APIRouter]):

        for router in routers:
            app.include_router(router)
            app.bot = bot

            router.app = app
            router.bot = bot

