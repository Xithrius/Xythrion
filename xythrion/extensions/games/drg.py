from datetime import datetime, timedelta, timezone

from discord.ext.commands import Cog, group

from xythrion.bot import Xythrion
from xythrion.context import Context


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

    def next_weekday(self, weekday: int = 1) -> int:
        """
        Gets the unix timestamp of when the next Tuesday happens.

        Source: https://stackoverflow.com/a/6558571
        """
        now = datetime.now(tz=self.tzinfo)

        days_ahead = weekday - now.weekday()

        if days_ahead <= 0:
            days_ahead += 7

        delta = now + timedelta(days=days_ahead)

        return int(delta.timestamp())

    @drg.command(aliases=("weekly",))
    async def next_weekly(
        self, ctx: Context,
    ) -> None:
        """Time delta until the weekly quests reset."""
        weekly_timestamp = self.next_weekday()

        await ctx.send(f"Next weekly reset is in <t:{weekly_timestamp}:R>")
