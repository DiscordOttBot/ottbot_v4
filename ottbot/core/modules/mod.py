import time

import tanjun

from ottbot.core.bot import OttBot
from ottbot.core.utils.funcs import build_loaders

component, load_component, unload_component = build_loaders()


async def auto_kick_fortnite(bot: OttBot = tanjun.inject(type="OttBot")):
    members = await bot.rest.fetch_members(640562201001721856)
    for member in members:
        if (rpc := member.get_presence()) is not None:
            for act in rpc.activities:
                if "tarkov" in act.name:
                    await member.send(f"Please tell me if you got this message, its a test `{time.time()}`")
