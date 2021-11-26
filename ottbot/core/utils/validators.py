import tanjun
import hikari


def message_len_validator(length: int):
    def val(_: tanjun.abc.Context, event: hikari.GuildMessageCreateEvent):
        if event.message.content is not None:
            return len(event.message.content) < length
        return False

    return val
