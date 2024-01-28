from discord.ext.commands import Cog, group

from bot.bot import Xythrion
from bot.context import Context
from bot.utils import is_trusted, remove_whitespace


class GraphExpression(Cog):
    """Graphing different kinds of data."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group()
    @is_trusted()
    async def graph(self, ctx: Context) -> None:
        """Group command for graphing."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    # TODO: Re-create a stable parser which also has sanitization of inputs, and is sandboxed
    @graph.command(aliases=("ex", "expr"), enabled=False)
    @is_trusted()
    async def expression(self, ctx: Context, *, expression: remove_whitespace) -> None:
        """Parse an expression into its components and graph it."""
        await ctx.send(expression)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(GraphExpression(bot))
