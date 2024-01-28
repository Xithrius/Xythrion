from datetime import datetime, timedelta

from discord.ext.commands import Cog, group

from bot.bot import Xythrion
from bot.context import Context


class Dates(Cog):
    """Arithmetic operations on dates."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @group(aliases=("date",))
    async def dates(self, ctx: Context) -> None:
        """Group command for dates."""
        await ctx.check_subcommands()


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
