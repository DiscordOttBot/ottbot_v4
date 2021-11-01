from abc import ABC, abstractmethod


class ICtx(ABC):
    ...

# ctx wrapper
#     hold more data
# ctx child
#     easier to pass and get hold of
# slash factory
#     automatically get bot and client as args