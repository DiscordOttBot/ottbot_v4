import typing as t
from abc import ABC, abstractmethod

_IClientT = t.TypeVar("_IClientT", bound="IClient")


class IClient(ABC):
    """Interface for the Tanjun Command Handler Client"""

    @abstractmethod
    def __init__(self: _IClientT, *args: t.Any, **kwargs: t.Any) -> None:
        self.errors: t.Optional[t.Any]
        self.embeds: t.Optional[t.Any]

    @abstractmethod
    def load_modules_(self: _IClientT) -> _IClientT:
        """Load slash command"""
