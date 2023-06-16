from xythrion.bot import Xythrion
from xythrion.extensions.games.drg import DeepRockGalactic


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading extensions within this folder."""
    await bot.add_cog(DeepRockGalactic(bot))
