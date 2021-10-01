import typing as t
from pathlib import Path

import tanjun
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

# from ottbot.abc.iclient import IClient

_ClientT = t.TypeVar("_ClientT", bound="OttClient")


class OttClient(tanjun.Client):
    """Attachable Client for slash commands"""

    __slots__ = tanjun.Client.__slots__ + ("scheduler",)

    def __init__(self: _ClientT, *args: t.Any, **kwards: t.Any) -> None:
        super().__init__(*args, **kwards)
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)

    def load_modules_(self: _ClientT) -> _ClientT:
        """Loads slash command modules"""
        return super().load_modules(
            *[
                f"ottbot.core.modules.{m.stem}"
                for m in Path(__file__).parent.glob("modules/*.py")
            ]
        )
        # Fixed in #55, need to wait until @task/components is merged.
        # return super().load_modules(*Path(__file__).parent.glob("modules/*.py"))
