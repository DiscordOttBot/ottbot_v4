from fastapi import APIRouter, FastAPI

from ottbot.core.bot import OttBot


class RouterWrapper(APIRouter):
    def __init__(self, **kwargs):
        self.__app: FastAPI = None
        self.__bot: OttBot = None

        super().__init__(**kwargs)

    @property
    def app(self) -> FastAPI:
        return self.__app

    @app.setter
    def app(self, app: FastAPI) -> None:
        if isinstance(app, FastAPI):
            self.__app = app
        else:
            raise TypeError(f"{app} must be of type FastAPI")

    @property
    def bot(self) -> OttBot:
        return self.__bot

    @bot.setter
    def bot(self, bot: OttBot) -> None:
        if isinstance(bot, OttBot):
            self.__bot = bot
        else:
            raise TypeError(f"{bot} must be of type OttBot")
