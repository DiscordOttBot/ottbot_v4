from abc import ABC, abstractmethod, abstractproperty
from fastapi import APIRouter
from ottbot.core.bot import OttBot


class IAPIWrapper(ABC):
    """Interface for the API Wrapper that holds the discord bot"""

    @abstractmethod
    def __init__(self, routers: list[APIRouter]) -> None:
        self.__bot: OttBot
        self.__routers: list[APIRouter]

    @abstractproperty
    def bot(self) -> OttBot:
        """Bot property for dynamic type checking"""

    @bot.setter
    def set_bot(self, bot: OttBot) -> None:
        """Bot setter for dynamic type checking"""

    @abstractproperty
    def routers(self) -> list[APIRouter]:
        """Routers property for dynamic type checking"""

    @routers.setter
    def set_data(self, routers: list[APIRouter]) -> None:
        """Routers setter for dynamic checking"""
