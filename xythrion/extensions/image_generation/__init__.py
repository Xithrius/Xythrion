from xythrion.bot import Xythrion
from xythrion.extensions.image_generation.gradients import GradientImageGenerator


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading extensions within this folder."""
    await bot.add_cog(GradientImageGenerator(bot))
