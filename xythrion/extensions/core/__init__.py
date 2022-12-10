from xythrion.bot import Xythrion
from xythrion.extensions.core.extensions import Extensions
from xythrion.extensions.core.warnings import Warnings


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading extensions within this folder."""
    await bot.add_cog(Extensions(bot))
    await bot.add_cog(Warnings(bot))
