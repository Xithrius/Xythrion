from xythrion.bot import Xythrion
from xythrion.extensions.core.administration import Administration
from xythrion.extensions.core.extensions import Extensions


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading extensions within this folder."""
    await bot.add_cog(Administration(bot))
    await bot.add_cog(Extensions(bot))
