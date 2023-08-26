from xythrion.bot import Xythrion
from xythrion.extensions.info.dates import Dates
from xythrion.extensions.info.links import Links
from xythrion.extensions.info.ping import Ping


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading extensions within this folder."""
    await bot.add_cog(Dates(bot))
    await bot.add_cog(Ping(bot))
    await bot.add_cog(Links(bot))
