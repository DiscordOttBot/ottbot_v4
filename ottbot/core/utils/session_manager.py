__all__: list[str] = ["SessionManager"]

import asyncio
import logging

import aiohttp
import tanjun
from hikari.impl import config

from ottbot.core.client import OttClient

_LOGGER = logging.getLogger("hikari.reinhard")


class SessionManager:
    """Utility class for managing an `aiohttp.ClientSession` type dependency."""

    __slots__ = ("http_timeout_settings", "proxy_settings", "_session", "user_agent")

    def __init__(
        self, http_timeout_settings: config.HTTPTimeoutSettings, proxy_settings: config.ProxySettings, user_agent: str
    ) -> None:
        self.http_timeout_settings = http_timeout_settings
        self.proxy_settings = proxy_settings
        self._session: aiohttp.ClientSession | None = None
        self.user_agent = user_agent

    def __call__(self) -> aiohttp.ClientSession:
        if not self._session:
            raise RuntimeError("Session isn't active")

        return self._session

    def load_into_client(self, client: tanjun.Client) -> None:
        """Add callbacks to the client for opening and closing the session"""

        if client.is_alive:
            raise RuntimeError("This should be loaded into the client before it has started.")

        client.add_client_callback(tanjun.ClientCallbackNames.STARTING, self.open).add_client_callback(
            tanjun.ClientCallbackNames.CLOSED, self.close
        )

    # TODO: switch over to tanjun.InjectorClient
    def open(self, client: OttClient = tanjun.inject(type=OttClient)) -> None:
        """Start the session.
        This will normally be called by a client callback.
        """
        if self._session:
            raise RuntimeError("Session already running")

        # Assert that this is only called within a live event loop
        asyncio.get_running_loop()
        self._session = aiohttp.ClientSession(
            headers={"User-Agent": self.user_agent},
            raise_for_status=False,
            timeout=aiohttp.ClientTimeout(
                connect=self.http_timeout_settings.acquire_and_connect,
                sock_connect=self.http_timeout_settings.request_socket_connect,
                sock_read=self.http_timeout_settings.request_socket_read,
                total=self.http_timeout_settings.total,
            ),
            trust_env=self.proxy_settings.trust_env,
        )
        client.set_type_dependency(aiohttp.ClientSession, self._session)
        _LOGGER.debug("acquired new aiohttp client session")

    async def close(self, client: tanjun.Client = tanjun.inject(type=tanjun.Client)) -> None:
        if not self._session:
            raise RuntimeError("Session not running")

        session = self._session
        self._session = None
        await session.close()
        client.remove_type_dependency(aiohttp.ClientSession)
