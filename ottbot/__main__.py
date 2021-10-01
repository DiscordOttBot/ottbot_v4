import os

from ottbot.core.bot import OttBot


def main() -> None:
    if os.name != "nt":
        import uvloop

        uvloop.install()

    bot: OttBot = OttBot()
    bot.run()



if __name__ == "__main__":
    main()
