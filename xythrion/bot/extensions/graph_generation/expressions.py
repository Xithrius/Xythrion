from bot.context import Context
from bot.utils import remove_whitespace
from discord.ext.commands import Cog, group, is_owner

from bot.bot import Xythrion


class GraphExpression(Cog):
    """Graphing different kinds of data."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group()
    @is_owner()
    async def graph(self, ctx: Context) -> None:
        """Group command for graphing."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @graph.command(aliases=("ex", "expr"))
    @is_owner()
    async def expression(self, ctx: Context, *, expression: remove_whitespace) -> None:
        """Parse an expression into its components and graph it."""
        await ctx.send(expression)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(GraphExpression(bot))