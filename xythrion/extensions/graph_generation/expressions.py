from discord.ext.commands import Cog, group, is_owner

from xythrion.bot import Xythrion
from xythrion.context import Context
from xythrion.utils import remove_whitespace


class GraphExpression(Cog):
    """Graphing different kinds of data."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group()
    @is_owner()
    async def graph(self, ctx: Context) -> None:
        """Group command for graphing."""
        if ctx.invoked_subcommand is None:
            await ctx.reply("Missing subcommand")

    @graph.command(aliases=("ex", "expr"))
    @is_owner()
    async def expression(
        self, ctx: Context, *, expression: remove_whitespace
    ) -> None:
        """Parse an expression into its components and graph it."""
        await ctx.send(expression)
