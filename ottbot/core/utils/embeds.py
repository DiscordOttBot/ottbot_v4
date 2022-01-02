from __future__ import annotations

import datetime
import typing as t

import hikari
import tanjun
import tanjun.abc

from ottbot.abc.iembeds import IEmbeds

FieldsT = t.Optional[list[tuple[t.Union[str, int], t.Union[str, int], bool]]]
ResourceishT = t.Optional[hikari.Resourceish]
ESCAPE_NAME: t.Final = "None"


class Embeds(IEmbeds):
    """Embed factory"""

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

        self.fields: FieldsT = fields
        self._ctx = ctx
        self.title = title
        self.desc = description
        self.footer = footer
        self.header = header
        self.header_url = header_url
        self.header_icon = header_icon
        self.thumbnail = thumbnail
        self.image = image
        self.color = color
        self.time: datetime.datetime = timestamp if timestamp is not None else datetime.datetime.now().astimezone()

    def _construct(self) -> hikari.Embed:
        """Construct base embed"""

        if isinstance(self._ctx, tanjun.abc.Context):
            embed = hikari.Embed(
                title=self.title,
                description=self.desc,
                timestamp=self.time,
                color=self.color or hikari.Color.from_hex_code("#713dc7"),
            )
            embed.set_thumbnail(self.thumbnail)
            embed.set_image(self.image)
            embed.set_author(name=self.header, url=self.header_url, icon=self.header_icon)

            embed.set_footer(
                text=(
                    None
                    if self.footer == ESCAPE_NAME
                    else (self.footer or f"Invoked by: {self._ctx.author.username}" if self._ctx is not None else "")
                ),
                icon=(
                    None
                    if self.footer == ESCAPE_NAME
                    else (self._ctx.author.avatar_url or (self._ctx.client.bot.get_me().avatar_url))  # type: ignore
                ),
            )

            return embed
        raise ValueError(f"Invalid Context: {self._ctx}")

    def _add_content(self, embed):
        """Add content fields to embed"""

        if self.fields:
            for name, value, inline in self.fields:
                embed.add_field(name=name, value=value, inline=inline)

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
        """Builds an embed from given kwargs."""

        self._init(
            ctx=ctx,
            title=title,
            description=description,
            fields=fields,
            footer=footer,
            header=header,
            header_url=header_url,
            header_icon=header_icon,
            thumbnail=thumbnail,
            image=image,
            color=color,
            timestamp=timestamp,
        )
        embed = self._construct()
        self._add_content(embed)

        return embed
