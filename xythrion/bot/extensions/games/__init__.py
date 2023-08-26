from xythrion.bot import Xythrion
from xythrion.extensions.games.drg import DeepRockGalactic
from xythrion.extensions.games.minecraft import MinecraftDistances, MinecraftStacks


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading extensions within this folder."""
    await bot.add_cog(DeepRockGalactic(bot))
    await bot.add_cog(MinecraftDistances(bot))
    await bot.add_cog(MinecraftStacks(bot))
