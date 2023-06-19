from datetime import datetime, timedelta, timezone

from discord.ext.commands import Cog, group

from xythrion.bot import Xythrion
from xythrion.context import Context

WEEKDAY_INDEX_RESET = 3
HOUR_RESET = 11


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
            await ctx.reply("Missing subcommand")

    def next_reset(self) -> int:
        """
        Gets the unix timestamp of the next Thursday 11am.

        Source: https://stackoverflow.com/a/6558571
        """
        now = datetime.now(tz=self.tzinfo)

        days_ahead = WEEKDAY_INDEX_RESET - now.weekday()
        hours_ahead = HOUR_RESET - now.hour

        if days_ahead <= 0:
            days_ahead += 7

        if hours_ahead <= 0:
            hours_ahead += 24

        delta = now + timedelta(days=days_ahead, hours=hours_ahead)

        return int(delta.timestamp())

    @drg.command(aliases=("weekly",))
    async def next_weekly(self, ctx: Context) -> None:
        """Time delta until the weekly quests reset."""
        weekly_timestamp = self.next_weekday()

        await ctx.send(f"Next weekly reset is in <t:{weekly_timestamp}:R>")
