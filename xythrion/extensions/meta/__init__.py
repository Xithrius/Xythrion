from xythrion.bot import Xythrion
from xythrion.extensions.meta.links import Links


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading in cogs within this folder."""
    await bot.add_cog(Links(bot))
