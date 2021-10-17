from fastapi import APIRouter, status
import requests

from ottbot.config import Config

URL = Config["DISCORD_API_URL"]  # http://discord.com/api/v9/
TOKEN = Config["TOKEN"]

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/{id_}", status_code=status.HTTP_200_OK)
def user_get(id_: int):
    response: requests.Response = requests.get(
        f"{URL}/users/{id_}", headers={"Authorization": f"Bot {TOKEN}"}
    )
    return response.json()
