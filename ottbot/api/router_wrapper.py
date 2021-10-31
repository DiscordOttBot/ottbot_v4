import typing as t

from fastapi import APIRouter, FastAPI

from ottbot.abc.irouter_wrapper import IRouterWrapper
from ottbot.core.bot import OttBot


class RouterWrapper(APIRouter, IRouterWrapper):
    def __init__(self, **kwargs):
        self.__app: t.Optional[FastAPI] = None
        self.__bot: t.Optional[OttBot] = None

        super().__init__(**kwargs)

    @property
    def app(self) -> FastAPI:
        if self.__app is not None:
            return self.__app
        raise ValueError("The router does not have an API attached to it yet")

    @app.setter
    def app(self, app: FastAPI) -> None:
        if isinstance(app, FastAPI):
            self.__app = app
        else:
            raise TypeError(f"{app} must be of type FastAPI")

    @property
    def bot(self) -> OttBot:
        if self.__bot is not None:
            return self.__bot
        raise ValueError("The router does not have a Bot attached to it yet")

    @bot.setter
    def bot(self, bot: OttBot) -> None:
        if isinstance(bot, OttBot):
            self.__bot = bot
        else:
            raise TypeError(f"{bot} must be of type OttBot")
