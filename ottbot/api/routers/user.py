import logging
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from hikari.users import UserImpl

from ottbot.config import Config
from ottbot.api.router_wrapper import RouterWrapper
from ottbot.core.utils.funcs import to_dict, convert2serialize

URL = Config["DISCORD_API_URL"]  # http://discord.com/api/v9/
TOKEN = Config["TOKEN"]

router = RouterWrapper(prefix="/user", tags=["Users"])


@router.get("/{id_}", status_code=status.HTTP_200_OK)
async def user_get(id_: int):
    """
    {
        "id": "418272575735595028",
        "username": "Amp",
        "avatar": "aa670a6f5df7f1523bcc047401fa85a8",
        "discriminator": "7452",
        "public_flags": 128,
        "banner": null,
        "banner_color": "#004ae4",
        "accent_color": 19172
    }
    """

    user = await router.bot.rest.fetch_user(id_)
    router.bot.logger.critical(convert2serialize(user))
    return to_dict(user)
    # if user:
    #     ret = {
    #         "id": user.id,
    #         "username": user.username,
    #         "avatar": user.avatar_hash,
    #         "discriminator": user.discriminator,
    #         "public_flags": user.flags.value,
    #     }
    # else:
    #     user = router.bot.cache.get_user(id_)
    #     ret = {
    #         "id": user.id,
    #         "username": user.username,
    #         "avatar": user.avatar_hash,
    #         "discriminator": user.discriminator,
    #         "public_flags": user.flags.value,
    #     }
    # return ret
