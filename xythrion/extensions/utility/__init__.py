from xythrion.bot import Xythrion
from xythrion.extensions.utility.links import Links
from xythrion.extensions.utility.ping import Ping


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading extensions within this folder."""
    await bot.add_cog(Ping(bot))
    await bot.add_cog(Links(bot))
