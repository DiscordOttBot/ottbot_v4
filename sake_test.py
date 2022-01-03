import asyncio
import os

import hikari
import sake
import dotenv

dotenv.load_dotenv()

bot = hikari.GatewayBot(token=os.environ["TOKEN"].split(":")[-1], intents=hikari.Intents.ALL)
# Initiate a self-managing cache with all supplied resources.
cache = sake.redis.RedisCache(
    app=bot,
    # The Hikari RESTAware client to be used when marshalling objects and making internal requests.
    event_manager=bot.event_manager,
    # The second positional argument may either be a Hikari DispatcherAware client or None.
    # When DispatcherAware is passed here the client will register it's own event listeners when started.
    # address=os.environ["REDIS_ADDRESS"],
    address="redis://127.0.0.1"
    # password=os.environ["REDIS_PASSWORD"],
)

prefix = "!"


@bot.listen()
async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
    if not event.message.content or not event.message.content.startswith(prefix) or not event.is_human:
        return
    arguments = event.message.content[len(prefix) :].split()
    if arguments[0] == "member":
        if not event.message.guild_id:
            await event.message.respond("Cannot use this command in a DM")
            return
        try:
            member = await cache.get_member(event.message.guild_id, int(arguments[1]))

        except sake.errors.EntryNotFound:
            await event.message.respond(content="Member not found.")
            member = await bot.rest.fetch_member(event.get_guild(), int(arguments[1]))

            old_name = member.display_name
            await member.edit(nick="asdf")
            await member.edit(nick=old_name)

        except ValueError:
            await event.message.respond(content="Invalid ID passed.")

        except IndexError:
            await event.message.respond(content="Missing ID.")

        else:
            embed = (
                hikari.Embed(title=f"Member: {member}")
                .set_thumbnail(member.avatar_url)
                .add_field(name="Joined server", value=member.joined_at.strftime("%d/%m/%y %H:%M %|"))
                .add_field(name="Roles", value=",".join(map(str, member.role_ids)))
                .add_field(name="Is bot", value=str(member.is_bot).lower())
            )
            await event.message.respond(embed=embed)


def main():
    asyncio.run(cache.open())
    bot.run()


if __name__ == "__main__":
    main()
