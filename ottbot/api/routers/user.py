import hikari
from fastapi import status

from ottbot.api.router_wrapper import RouterWrapper
from ottbot.core.utils.funcs import to_dict

router: RouterWrapper = RouterWrapper(prefix="/user", tags=["Users"])


@router.get("/{id_}", status_code=status.HTTP_200_OK)
async def user_get(id_: int):
    """Returns a JSON representation of a user"""

    user: hikari.User = await router.bot.rest.fetch_user(id_)
    return to_dict(user)
