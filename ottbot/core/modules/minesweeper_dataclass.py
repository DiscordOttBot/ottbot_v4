import asyncio
import itertools
import random
import typing as t
from dataclasses import dataclass

import hikari
import tanjun

from ottbot.core.client import OttClient

import logging


@dataclass
class Cell:
    index: int
    value: int
    revealed: bool = False

    @property
    def style(self) -> hikari.ButtonStyle:
        if self.revealed:
            if self.value == -1:
                return hikari.ButtonStyle.DANGER
            if self.value == -2:
                return hikari.ButtonStyle.SUCCESS
            return hikari.ButtonStyle.PRIMARY
        return hikari.ButtonStyle.SECONDARY

    def __str__(self) -> str:
        if self.revealed:
            if self.value == -1:
                return "\N{BOMB}"
            if 0 <= self.value <= 8:
                return f"{self.value}"
        return " "


class BoardStatus(int, hikari.internal.enums.Enum):
    PLAYING = 0
    LOST = 1
    WON = 2


class Board:
    def __init__(self, bombs: int) -> None:
        self.cells = []
        self.status = BoardStatus.PLAYING

        for k, x in enumerate(
            matrix := random.sample([0, 1], counts=[25 - bombs, bombs], k=25)
        ):
            if x:
                self.cells.append(Cell(k, -1))
                continue
            value = 0
            x, y = k // 5, k % 5
            for a in itertools.product(range(x - 1, x + 2), range(y - 1, y + 2)):
                if a != (x, y) and all(0 <= n < 5 for n in a):
                    # print(f"{matrix=}, {a=} | {a[0] * 5 + a[1]}")
                    if matrix[a[0] * 5 + a[1]]:
                        value += 1
            self.cells.append(Cell(k, value))

    def components(self, ctx: tanjun.abc.Context) -> list[hikari.impl.ActionRowBuilder]:
        rows = []
        for i in range(5):
            row = ctx.rest.build_action_row()
            for j in range(5):
                cell = self.cells[(k := i * 5 + j)]
                button = row.add_button(cell.style, f"{k}").set_label(f"{cell}")
                if self.status != BoardStatus.PLAYING:
                    button.set_is_disabled(True)
                button.add_to_container()

            rows.append(row)
        return rows

    def has_won(self) -> bool:
        for cell in self.cells:
            logging.info(f"      {cell.value} | {cell.revealed}")
            if cell.value == -1 and cell.revealed:
                return False
            if 0 <= cell.value <= 8 and not cell.revealed:
                return False

            return True

    def reveal(self, status: BoardStatus) -> None:
        self.status = status
        for cell in self.cells:
            cell.revealed = True


component = tanjun.Component()


@component.with_slash_command
@tanjun.with_int_slash_option("bombs", "The number of bombs", default=8)
@tanjun.as_slash_command("minesweeper", "Play Minesweeper")
async def minesweeper_cmd(ctx: tanjun.abc.Context, bombs: int) -> None:
    board = Board(bombs)
    await ctx.respond("**Minesweeper**", components=board.components(ctx))

    while True:
        try:
            event = await ctx.client.events.wait_for(
                hikari.InteractionCreateEvent, timeout=60
            )
            if not isinstance(event.interaction, hikari.ComponentInteraction):
                continue
        except asyncio.TimeoutError:
            await ctx.edit_initial_response(
                "**Minesweeper**\nYour game timed out.", components=[]
            )
        else:
            await event.interaction.create_initial_response(
                hikari.ResponseType.DEFERRED_MESSAGE_UPDATE
            )

            cell = board.cells[int(event.interaction.custom_id)]

            if cell.value == -1:
                board.reveal(BoardStatus.LOST)
                await ctx.edit_initial_response(
                    "**Minesweeper**\nGame over! You lost!",
                    components=board.components(ctx),
                )
            else:
                cell.revealed = True
                logging.info("SAFE -- MINES")
                logging.info(board.has_won())
                if board.has_won():
                    board.reveal(BoardStatus.WON)

                    for cell in board.cells:
                        if cell.value == -1:
                            cell.value = -2

                    await ctx.edit_initial_response(
                        "**Minesweeper**\nGame over! You Won!",
                        components=board.components(ctx),
                    )
                else:
                    await ctx.edit_initial_response(
                        "**Minesweeper**", components=board.components(ctx)
                    )

            if board.status != BoardStatus.PLAYING:
                break


@tanjun.as_loader
def load_component(client: OttClient) -> None:
    client.add_component(component.copy())
