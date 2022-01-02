import datetime
import typing as t
from abc import ABC, abstractmethod

import hikari
import tanjun

FieldsT = t.Optional[list[tuple[t.Union[str, int], t.Union[str, int], bool]]]
ResourceishT = t.Optional[hikari.Resourceish]


class IEmbeds(ABC):
    """Interface for the Bot's Embed factory"""

    @abstractmethod
    def _init(
        self,
        ctx: tanjun.abc.Context,
        title: str | None = None,
        description: str | None = None,
        fields: FieldsT = None,
        footer: str | None = None,
        header: str | None = None,
        header_url: str | None = None,
        header_icon: ResourceishT = None,
        thumbnail: ResourceishT = None,
        image: ResourceishT = None,
        color: hikari.Colorish | None = None,
        timestamp: datetime.datetime | None = None,
    ) -> None:
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
    def build(
        self,
        ctx: tanjun.abc.Context,
        title: str | None = None,
        description: str | None = None,
        fields: FieldsT = None,
        footer: str | None = None,
        header: str | None = None,
        header_url: str | None = None,
        header_icon: ResourceishT | None = None,
        thumbnail: ResourceishT = None,
        image: ResourceishT = None,
        color: hikari.Colorish | str | None = None,
        timestamp: datetime.datetime | None = None,
    ) -> hikari.Embed:
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
