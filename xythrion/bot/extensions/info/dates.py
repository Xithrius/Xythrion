from datetime import datetime, timedelta

from bot.context import Context
from discord.ext.commands import Cog, group

from bot.bot import Xythrion


class Dates(Cog):
    """Arithmetic operations on dates."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @group(aliases=("date",))
    async def dates(self, ctx: Context) -> None:
        """Group command for dates."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @dates.command()
    async def delta(self, ctx: Context, timestamp: int) -> None:
        now = int(datetime.now(tz=self.bot.tzinfo).timestamp())

        diff = now - timestamp

        d = timedelta(seconds=diff)
        when = datetime.fromtimestamp(timestamp, tz=self.bot.tzinfo)

        if diff <= 0:
            await ctx.send(f"It has been {d} since {when}")
        else:
            await ctx.send(f"It is {d} until {when}")


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Dates(bot))