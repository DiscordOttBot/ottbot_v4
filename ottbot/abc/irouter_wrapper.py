import typing as t
from abc import ABC, abstractproperty

from fastapi import FastAPI

from ottbot.core.bot import OttBot


class IRouterWrapper(ABC):
    """Inerface for RouterWrapper"""

    @abstractproperty
    def app(self) -> FastAPI:
        """App property for dynamic type checking"""
        raise NotImplementedError

    @app.setter
    def app(self, app: FastAPI) -> None:
        """App setter for dynamic type checking"""
        raise NotImplementedError

    @abstractproperty
    def bot(self) -> OttBot:
        """Bot property for dynamic type checking"""
        raise NotImplementedError

    @bot.setter
    def bot(self, bot: OttBot) -> None:
        """Bot setter for dynamic type checking"""
        raise NotImplementedError
