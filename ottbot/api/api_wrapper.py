from fastapi import APIRouter, FastAPI
from ottbot.core.bot import OttBot


class APIWrapper(FastAPI):
    def __init__(self, routers):
        self.__bot: OttBot = None
        self.__routers: list[APIRouter] = routers

        super().__init__()

    @property
    def bot(self) -> OttBot:
        return self.__bot

    @bot.setter
    def set_bot(self, bot: OttBot) -> None:
        if isinstance(bot, OttBot):
            self.__bot = bot
        else:
            raise TypeError(f"{bot} is not of type 'OttBot'")

    @property
    def routers(self) -> list[APIRouter]:

        return self.__routers

    @routers.setter
    def set_data(self, routers: list[APIRouter]) -> None:
        if all([isinstance(r, APIRouter) for r in routers]):
            self.__routers = routers
        else:
            raise TypeError(
                f"Invalid list of routers: {routers}. All elements of the list must be of type APIRouter"
            )
