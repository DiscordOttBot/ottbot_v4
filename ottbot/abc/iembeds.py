import typing as t
from abc import ABC, abstractmethod

import hikari


class IEmbed(ABC):
    """Interface for the Bot's Embed factory"""

    @abstractmethod
    def _init(self, **kwargs: dict[t.Any, t.Any]) -> None:
        """Initialize embed values"""
        raise NotImplementedError

    @abstractmethod
    def _construct(self):
        """Construct base embed"""
        raise NotImplementedError

    @abstractmethod
    def _add_content(self):
        """Add content fields to embed"""
        raise NotImplementedError

    @abstractmethod
    def build(self, **kwargs: dict[t.Any, t.Any]) -> hikari.Embed:
        """Builds an embed from given kwargs.
        kwargs:
            - ctx: required
            - title: optional
            - description: optional
            - fields: optional
            - footer: optional
            - header: optional
            - header_icon: optional
            - thumbnail: optional
            - image: optional
            - color: optional
        Returns:
            - hikari.Embed
        """
        raise NotImplementedError
