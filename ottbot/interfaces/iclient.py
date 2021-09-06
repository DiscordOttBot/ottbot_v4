import typing as t
from abc import ABC, abstractmethod

import tanjun

_IClientT = t.TypeVar("_IClientT", bound="IClient")

class IClient(ABC):
    """Interface for Client"""

    @abstractmethod
    def load_modules(self: _IClientT) -> _IClientT:
        pass