import hikari
import typing as t

EventT = t.Union[t.Type[hikari.StartingEvent], t.Type[hikari.StoppingEvent]]

async def on_starting(event: hikari.StartingEvent) -> None:
        """Runs before bot is connected. Blocks on_started until complete."""
        ...

e: EventT = hikari.StartingEvent

d: dict[EventT, t.Callable[..., t.Coroutine[t.Any, t.Any, None]]] = {hikari.StartingEvent: on_starting}


print(type(on_starting))
