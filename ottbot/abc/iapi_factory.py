from abc import ABC, abstractmethod

from fastapi import APIRouter, FastAPI

from ottbot.core.bot import OttBot


class IAPIFactory(ABC):
    """Interface Class for custom ReST API"""

    @staticmethod
    @abstractmethod
    def build(bot: OttBot, app: FastAPI, routers: list[APIRouter]) -> None:
        """Link the bot, api, and routers to each other"""
