from __future__ import annotations

import datetime
import typing as t

import hikari

import lightbulb
import tanjun
import tanjun.abc
from ottbot.abc.iembeds import IEmbed

FieldsT = t.Optional[list[tuple[t.Union[str, int], t.Union[str, int], bool]]]
CtxT = t.Union[lightbulb.Context, tanjun.abc.Context]
ResourceishT = t.Optional[hikari.files.Resourceish]

ESCAPE_NAME: t.Final = "None"


class Embeds(IEmbed):
    """Embed factory"""

    def _init(self, **kwargs: t.Any) -> None:
        """Initialize embed values"""

        self.fields: FieldsT = kwargs.get("fields")
        self._ctx: t.Union[CtxT, t.Any, None] = kwargs.get("ctx")
        self.title: t.Optional[str] = kwargs.get("title")
        self.desc: t.Optional[str] = kwargs.get("description")
        self.footer: t.Optional[str] = kwargs.get("footer")
        self.header: t.Optional[str] = kwargs.get("header")
        self.header_url: t.Optional[str] = kwargs.get("header_url")
        self.header_icon: ResourceishT = kwargs.get("header_icon")
        self.thumbnail: ResourceishT = kwargs.get("thumbnail")
        self.image: ResourceishT = kwargs.get("image")
        self.color: t.Optional[hikari.colors.Colorish] = kwargs.get("color")
        self.time: datetime.datetime = kwargs.get(
            "timestamp", datetime.datetime.now().astimezone()
        )

    def _construct(self) -> hikari.Embed:
        """Construct base embed"""

        if isinstance(self._ctx, tanjun.abc.Context) or isinstance(
            self._ctx, lightbulb.Context
        ):
            embed = hikari.Embed(
                title=self.title,
                description=self.desc,
                timestamp=self.time,
                color=self.color or hikari.Color.from_hex_code("#713dc7"),
            )
            embed.set_thumbnail(self.thumbnail)
            embed.set_image(self.image)
            embed.set_author(
                name=self.header, url=self.header_url, icon=self.header_icon
            )

            embed.set_footer(
                text=(
                    None
                    if self.footer == ESCAPE_NAME
                    else (self.footer or f"Invoked by: {self._ctx.author.username}")
                ),
                icon=(
                    None
                    if self.footer == ESCAPE_NAME
                    else (
                        self._ctx.author.avatar_url or (self._ctx.client.bot.get_me().avatar_url)  # type: ignore
                    )
                ),
            )

            return embed
        raise ValueError(f"Invalid Context: {self._ctx}")

    def _add_content(self, embed):
        """Add content fields to embed"""

        if self.fields:
            for name, value, inline in self.fields:
                embed.add_field(name=name, value=value, inline=inline)

    def build(self, **kwargs: t.Any) -> hikari.Embed:
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

        self._init(**kwargs)
        embed = self._construct()
        self._add_content(embed)

        return embed
