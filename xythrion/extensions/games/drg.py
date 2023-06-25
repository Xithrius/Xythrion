from datetime import datetime, timedelta, timezone

from croniter import croniter
from discord.ext.commands import Cog, group

from xythrion.bot import Xythrion
from xythrion.context import Context

WEEKLY_CRON = "00 11 * * THU"


class DeepRockGalactic(Cog):
    """Information about the game 'Deep Rock Galactic'."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

        # https://stackoverflow.com/a/30712187
        timezone_offset: float = 0.0
        self.tzinfo = timezone(timedelta(hours=timezone_offset))

    @group(aliases=("deeprockgalactic",))
    async def drg(self, ctx: Context) -> None:
        """Group command for Deep Rock Galactic."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    def next_reset(self) -> int:
        """
        Gets the unix timestamp of the next Thursday 11am.

        Source: https://stackoverflow.com/a/6558571
        """
        now = datetime.now(tz=self.tzinfo)

        next_thursday = croniter(WEEKLY_CRON, now).get_next(datetime)

        return int(next_thursday.timestamp())

    @drg.command(aliases=("weekly",))
    async def next_weekly(self, ctx: Context) -> None:
        """Time delta until the weekly quests reset."""
        weekly_timestamp = self.next_reset()

        await ctx.send(f"Next weekly reset is in <t:{weekly_timestamp}:R>")
