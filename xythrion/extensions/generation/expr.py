import ast
from typing import Union

import numpy as np
from discord.ext.commands import Cog, group, is_owner, Context
from discord import Embed, File

from xythrion.bot import Xythrion
from xythrion.utils import remove_whitespace


class GraphExpression(Cog):
    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group()
    @is_owner()
    async def graph(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.reply("Missing subcommand")

    @graph.command(aliases=("ex", "expr"))
    @is_owner()
    async def expression(
        self, ctx: Context, *, expression: remove_whitespace
    ) -> None:
        await ctx.send(expression)
