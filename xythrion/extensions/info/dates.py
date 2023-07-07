from datetime import datetime, timedelta, timezone

from discord.ext.commands import Cog, group

from xythrion.bot import Xythrion
from xythrion.context import Context


class Dates(Cog):
    """Arithmetic operations on dates."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

        # https://stackoverflow.com/a/30712187
        timezone_offset: float = 0.0
        self.tzinfo = timezone(timedelta(hours=timezone_offset))

    @group(aliases=("date",))
    async def dates(self, ctx: Context) -> None:
        """Group command for dates."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @dates.command()
    async def delta(self, ctx: Context, timestamp: int) -> None:
        now = int(datetime.now(tz=self.tzinfo).timestamp())

        diff = now - timestamp

        d = timedelta(seconds=diff)
        when = datetime.fromtimestamp(timestamp, tz=self.tzinfo)

        if diff <= 0:
            await ctx.send(f"It has been {d} since {when}")
        else:
            await ctx.send(f"It is {d} until {when}")
