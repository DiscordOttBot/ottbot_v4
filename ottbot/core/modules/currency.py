import random
from datetime import datetime

import hikari
import tanjun

from ottbot.core.db.db import AsyncPGDatabase
from ottbot.core.utils.funcs import build_loaders

component, load_component, unload_component = build_loaders()

currency_group = component.with_slash_command(tanjun.slash_command_group("currency", "Currency related commands"))


async def get_bal(db: AsyncPGDatabase, user_id: int) -> int:
    """Get the balance of a user if they exist or create a new one."""
    bal = await db.fetch("SELECT balance FROM currency WHERE user_id = $1", user_id)
    if bal is None:
        await db.execute("INSERT INTO currency (user_id) VALUES ($1)", user_id)
        bal = 0
    return bal


async def set_bal(db: AsyncPGDatabase, user_id: int, bal: int) -> None:
    """Set the balance of a user."""
    await db.execute("UPDATE currency SET balance = $1 WHERE user_id = $2", bal, user_id)


async def get_bank(db: AsyncPGDatabase, user_id: int) -> int:
    """Get the bank of a user if they exist or create a new one."""
    bank = await db.fetch("SELECT bank FROM currency WHERE user_id = $1", user_id)
    if bank is None:
        await db.execute("INSERT INTO currency (user_id) VALUES ($1)", user_id)
        bank = 0
    return bank


async def set_bank(db: AsyncPGDatabase, user_id: int, bank: int) -> None:
    """Set the bank of a user."""
    await db.execute("UPDATE currency SET bank = $1 WHERE user_id = $2", bank, user_id)


@currency_group.with_command
@tanjun.with_member_slash_option("member", "The member to check the balance of.", default=None)
@tanjun.as_slash_command("bal", "Check the balance of the user")
async def cmd_bal(
    ctx: tanjun.abc.SlashContext,
    member: hikari.Member | None,
    db: AsyncPGDatabase = tanjun.inject(type=AsyncPGDatabase),
) -> None:
    if ctx.guild_id is None:
        return
    id = member.id if member else ctx.author.id
    bal = await get_bal(db, id)
    bank = await get_bank(db, id)
    await ctx.respond(f"Balance is {bal}, bank is {bank}")


@currency_group.with_command
@tanjun.as_slash_command("daily", "Claim your daily currency.")
async def cmd_daily(ctx: tanjun.abc.SlashContext, db: AsyncPGDatabase = tanjun.inject(type=AsyncPGDatabase)) -> None:
    if ctx.guild_id is None:
        return

    bal = await get_bal(db, ctx.author.id)
    last_daily: datetime | None = await db.fetch("SELECT last_daily FROM currency WHERE user_id = $1", ctx.author.id)
    if last_daily is not None:
        if datetime.now().timestamp() - (last := last_daily.timestamp()) < 86400:
            await ctx.respond(f"You already claimed your daily! You can claim it again at <t:{last + 86400:.0f}:t>")
            return

    new_bal = bal + 1  # TODO: change how bal is calculated
    await set_bal(db, ctx.author.id, new_bal)

    await ctx.respond(f"Your new balance is {new_bal}")


@currency_group.with_command
@tanjun.as_slash_command("dice", "Roll dice for currency")
async def cmd_(ctx: tanjun.abc.SlashContext, db: AsyncPGDatabase = tanjun.inject(type=AsyncPGDatabase)) -> None:
    if ctx.guild_id is None:
        return
    roll = random.randint(1, 6)
    new_bal = await get_bal(db, ctx.author.id) + roll
    await set_bal(db, ctx.author.id, new_bal)
    await ctx.respond(f"You rolled a {roll} and now have {new_bal} currency!")


@currency_group.with_command
@tanjun.with_int_slash_option("number", "The number that you are guessing")
@tanjun.as_slash_command("guess", "Guess a number between 1 and 100 for currency")
async def cmd_guess(
    ctx: tanjun.abc.SlashContext, number: int, db: AsyncPGDatabase = tanjun.inject(type=AsyncPGDatabase)
) -> None:
    if ctx.guild_id is None:
        return
    if 1 > number > 100:
        await ctx.respond("The number must be between 1 and 100")
        return

    rand = random.randint(1, 100)
    if number == rand:
        await ctx.respond("Congratulations! You guessed the number! You win 10 currency!")
        bal = await get_bal(db, ctx.author.id) + 10
        await set_bal(db, ctx.author.id, bal)
        return
    if number == rand + 1 or number == rand - 1:
        await ctx.respond(
            f"Almost! You guessed 1 {'below' if rand > number else 'above' } the number! You win 5 currency!"
        )
        bal = await get_bal(db, ctx.author.id) + 5
        await set_bal(db, ctx.author.id, bal)
        return
    await ctx.respond(f"You guessed {number} and the number was {rand}. Better luck next time!")


@currency_group.with_command
@tanjun.with_str_slash_option("amount", "The amount to deposit, or 'all' to deposit all your balance")
@tanjun.as_slash_command("deposit", "Deposit currency into your bank")
async def cmd_deposit(
    ctx: tanjun.abc.SlashContext, amount: str, db: AsyncPGDatabase = tanjun.inject(type=AsyncPGDatabase)
) -> None:
    if ctx.guild_id is None:
        return

    bal = await get_bal(db, ctx.author.id)
    if amount.lower() == "all":
        deposit = bal
        await set_bal(db, ctx.author.id, 0)
    else:
        deposit = int(amount)
        if deposit > bal:
            await ctx.respond("You don't have that much currency!")
            return
        await set_bal(db, ctx.author.id, bal - deposit)

    bank = await get_bank(db, ctx.author.id)
    await set_bank(db, ctx.author.id, deposit + bank)
    await ctx.respond(f"Deposited {deposit} currency into your bank. Your new bank balance is {deposit + bank}")


@currency_group.with_command
@tanjun.with_int_slash_option("amount", "the amount to set")
@tanjun.with_member_slash_option("member", "the member to set the balance of", default=None)
@tanjun.as_slash_command("set", "Set the balance of a user")
async def cmd_set(
    ctx: tanjun.abc.SlashContext,
    amount: int,
    member: hikari.Member,
    db: AsyncPGDatabase = tanjun.inject(type=AsyncPGDatabase),
) -> None:
    if ctx.guild_id is None:
        return

    id = member.id if member else ctx.author.id
    await get_bal(db, id)  # Make sure the user exists
    await set_bal(db, id, amount)
    await ctx.respond(f"Set your balance to {amount}")


# TODO: Add message triggered games
# @component.with_listener(hikari.GuildMessageCreateEvent)
# async def foo(event: hikari.GuildMessageCreateEvent):
#     print(f"GMCE: {event.message.content}")
#     ...


# TODO: Award currnecy to someone who comes up with the name of the currency

"""
Prestige system

- bank has a max amount per level
- pay / give items to level up
- once you reach a certain level you can prestige
gain items through shop / loot boxes

presige resets all currency and some items but gives a currency boost

gain roles based on prestige level


Commands

bal
daily

MEE6:
Commands
/buy
Buy any item from the shop

/daily
Claim your daily coins

/coins
Get the coins amount of anyone in the server

/dice
Throw two dice to gain coins

/economy-info
Everything you need to know about the economy of the server

/games
Get more info about server's games

/give-coins
Give coins to anyone in the server

/give-item
Give an item from your inventory to a member

/guess
Play Guess the number to gain coins

/items
List the items you bought from the shop

/remove-coins
Remove coins from anyone in the server

/remove-item
Remove an item from someone's inventory

/richest
Get the richest players of the server

/rps
Play rock paper scissors to gain coins

/roulette
Play roulette to gain coins

/shop
List items from the shop

/spawn-item
Spawn an item in someone's inventory

/use
Use an item from your inventory

/work
Work for one hour and come back to claim your paycheck



https://dankmemer.lol/commands

"""
