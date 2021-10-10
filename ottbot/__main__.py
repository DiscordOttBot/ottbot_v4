import os

from ottbot.core.bot import OttBot, _BotT


def main() -> None:
    if os.name != "nt":
        import uvloop

        uvloop.install()

    bot: OttBot = OttBot(version="4.0.0")
    bot.run()


if __name__ == "__main__":
    main()
