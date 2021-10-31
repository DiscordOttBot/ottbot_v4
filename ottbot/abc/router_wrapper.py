import typing as t
from abc import ABC, abstractproperty

from fastapi import APIRouter, FastAPI

from ottbot.core.bot import OttBot


class RouterWrapper(ABC):
    def __init__(self, **kwargs: dict[t.Any, t.Any]) -> None:
        self.__app: FastAPI
        self.__bot: OttBot

    @abstractproperty
    def app(self) -> FastAPI:
        """App property for dynamic type checking"""

    @app.setter
    def app(self, app: FastAPI) -> None:
        """App setter for dynamic type checking"""

    @abstractproperty
    def bot(self) -> OttBot:
        """Bot property for dynamic type checking"""

    @bot.setter
    def bot(self, bot: OttBot) -> None:
        """Bot setter for dynamic type checking"""
