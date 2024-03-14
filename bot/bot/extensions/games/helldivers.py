from discord.ext.commands import Cog

from bot.bot import Xythrion


class HellDivers(Cog):
    """HellDivers 2 Cog."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(HellDivers(bot))
