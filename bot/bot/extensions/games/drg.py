from datetime import datetime, timedelta

from discord.ext.commands import Cog, group
from humanize import naturaldelta

from bot.bot import Xythrion
from bot.context import Context


class DeepRockGalactic(Cog):
    """Deep Rock Galactic info cog."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group(aliases=("drg",))
    async def deep_rock_galactic(self, ctx: Context) -> None:
        """Group command for Deep Rock Galactic."""
        await ctx.check_subcommands()

    @deep_rock_galactic.command(aliases=("weekly_quests", "weekly"))
    async def weekly_reset(self, ctx: Context) -> None:
        today = datetime.now(tz=self.bot.tzinfo)
        days_until_next_thursday = (3 - today.weekday() + 7) % 7
        next_thursday = today + timedelta(days=days_until_next_thursday)
        next_thursday = next_thursday.replace(
            hour=11,
            minute=0,
            second=0,
            microsecond=0,
        )

        time_until_next_thursday = next_thursday - today

        delta = naturaldelta(time_until_next_thursday.total_seconds())

        await ctx.send(f"Weekly quests reset in {delta}")


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(DeepRockGalactic(bot))
