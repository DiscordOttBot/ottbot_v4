from abc import ABC, abstractmethod, abstractproperty

from fastapi import APIRouter

from ottbot.core.bot import OttBot


class IAPIWrapper(ABC):
    """Interface for the API Wrapper that holds the discord bot"""


    @abstractproperty
    def bot(self) -> OttBot:
        """Bot property for dynamic type checking"""
        raise NotImplementedError

    @bot.setter
    def bot(self, bot: OttBot) -> None:
        """Bot setter for dynamic type checking"""
        raise NotImplementedError

    @abstractproperty
    def routers(self) -> list[APIRouter]:
        """Routers property for dynamic type checking"""
        raise NotImplementedError
 
    @routers.setter
    def routers(self, routers: list[APIRouter]) -> None:
        """Routers setter for dynamic checking"""
        raise NotImplementedError
