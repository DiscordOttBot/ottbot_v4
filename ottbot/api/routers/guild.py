import requests
from fastapi import status

from ottbot import Config
from ottbot.api.router_wrapper import RouterWrapper
from ottbot.core.utils.funcs import to_dict

router: RouterWrapper = RouterWrapper(prefix="/guild", tags=["Guilds"])


@router.get("/{id_}/roles")
async def get_guild_roles(id_: int):
    """
    Get the roles of a guild
    :param id_: Guild ID
    :return: List of roles
    """
    guild = await router.bot.rest.fetch_guild(id_)
    if guild is None:
        return status.HTTP_404_NOT_FOUND
    roles = await guild.fetch_roles()
    return [to_dict(role) for role in roles]


# @router.get("/{id_}/members")
# async def get_guild_members(id_: int):
#     """
#     Get the members of a guild
#     :param id_: Guild ID
#     :return: List of members
#     """
#     guild = await router.bot.rest.fetch_guild(id_)
#     if guild is None:
#         return status.HTTP_404_NOT_FOUND


# @router.get("/{id_}/channels")
# async def get_guild_channels(id_: int):
#     """
#     Get the channels of a guild
#     :param id_: Guild ID
#     :return: List of channels
#     """
#     guild = await router.bot.rest.fetch_guild(id_)
#     if guild is None:
#         return status.HTTP_404_NOT_FOUND


# @router.get("/{id_}/emojis")
# async def get_guild_emojis(id_: int):
#     """
#     Get the emojis of a guild
#     :param id_: Guild ID
#     :return: List of emojis
#     """
#     guild = await router.bot.rest.fetch_guild(id_)
#     if guild is None:
#         return status.HTTP_404_NOT_FOUND
#     return guild.emojis


# @router.get("/{id_}/icon")
# async def get_guild_icon(id_: int):
#     """
#     Get the icon of a guild
#     :param id_: Guild ID
#     :return: Icon
#     """
#     guild = await router.bot.rest.fetch_guild(id_)
#     if guild is None:
#         ...


# @router.get("/{id_}", status_code=status.HTTP_200_OK)
# async def guild_get(id_: int):
#     """Returns a JSON representation of a guild"""

#     guild: hikari.Guild = await router.bot.rest.fetch_guild(id_)
#     return to_dict(guild)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all():
    """Returns a list of guilds"""
    r = requests.get(
        "http://discord.com/api/v8/users/@me/guilds",
        headers={"Authorization": f"Bot {Config['TOKEN', str]}"},
    )
    if r.status_code == 200:
        return r.json()
    else:
        return {"error": f"{r.status_code}"}

    # guilds = router.bot.rest.fetch_my_guilds()
    # print(guilds)
    # d = dict()
    # async for guild in guilds:
    #     d[guild.id] = to_dict(guild)
    #     await asyncio.sleep(1)
    # TODO: Change back after discord fixes chunking requests
    # return d
    # return {guild.id: to_dict(guild) async for guild in guilds}


# @router.post("/{id_}/ban/{user_id_}", status_code=status.HTTP_200_OK)
# async def user_ban(id_: int, user_id_: int):
#     """Bans and returns a user from the guild"""

#     try:
#         user = await router.bot.rest.fetch_user(user_id_)
#         await router.bot.rest.ban_user(id_, user_id_)
#     except HTTPException:
#         return {"error": "User not found"}
#     return {"success": True, "user": user}
