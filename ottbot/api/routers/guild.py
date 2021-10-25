import logging

from fastapi import status
from fastapi.exceptions import HTTPException
import hikari

from ottbot.api.router_wrapper import RouterWrapper
from ottbot.core.utils.funcs import to_dict


router: RouterWrapper = RouterWrapper(prefix="/guild", tags=["Guilds"])


@router.get("/{id_}", status_code=status.HTTP_200_OK)
async def user_get(id_: int):
    """Returns a JSON representation of a guild"""

    guild: hikari.Guild = await router.bot.rest.fetch_guild(id_)
    router.bot.logger.critical(guild)
    return to_dict(guild)
