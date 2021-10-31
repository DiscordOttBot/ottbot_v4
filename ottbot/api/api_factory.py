from fastapi import APIRouter

from ottbot.api.api_wrapper import APIWrapper
from ottbot.api.router_wrapper import RouterWrapper
from ottbot.core.bot import OttBot
from ottbot.abc.iapi_factory import IAPIFactory

class APIFactory(IAPIFactory):
    @staticmethod
    def build(bot: OttBot, app: APIWrapper, routers: list[RouterWrapper]) -> None:

        for router in routers:
            app.include_router(router)
            app.bot = bot

            router.app = app
            router.bot = bot
