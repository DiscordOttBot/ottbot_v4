import typing as t

from hikari.colors import Color

# SERVER_ID: int = 545984256640286730
SERVER_ID: int = 640562201001721856

DELETE_CUSTOM_ID: str = "AUTHOR_DELETE_BUTTON:"

FAILED_COLOUR: t.Final[Color] = Color(0xF04747)
PASS_COLOUR: t.Final[Color] = Color(0x43B581)

WHITE: t.Final[Color] = Color(0xFFFFFE)  # 0xFFFFFF is treated as no colour in embeds by Discord.

ZWJ: t.Final[str] = "\u200d"
