from fastapi import APIRouter, FastAPI

from ottbot.abc.iapi_wrapper import IAPIWrapper
from ottbot.core.bot import OttBot


class APIWrapper(FastAPI, IAPIWrapper):
    """API Wrapper that holds the discord bot"""

    def __init__(self, routers):
        self.__bot: OttBot | None = None
        self.__routers: list[APIRouter] = routers

        super().__init__()

    @property
    def bot(self) -> OttBot:
        if self.__bot is not None:
            return self.__bot
        raise ValueError("No Bot object is set")

    @bot.setter
    def bot(self, bot: OttBot) -> None:
        if isinstance(bot, OttBot):
            self.__bot = bot
        else:
            raise TypeError(f"{bot} is not of type 'OttBot'")

    @property
    def routers(self) -> list[APIRouter]:
        return self.__routers

    @routers.setter
    def routers(self, routers: list[APIRouter]) -> None:
        if all([isinstance(r, APIRouter) for r in routers]):
            self.__routers = routers
        else:
            raise TypeError(
                f"Invalid list of routers: {routers}. All elements of the list must be of type APIRouter"
            )
