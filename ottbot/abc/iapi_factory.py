from abc import ABC, abstractstaticmethod

from fastapi import APIRouter, FastAPI

from ottbot.core.bot import OttBot


class IAPIFactory(ABC):
    """Interface Class for custom ReST API"""

    @abstractstaticmethod
    def build(bot: OttBot, app: FastAPI, routers: list[APIRouter]):
        """Link the bot, api, and routers to each other"""
        ...
