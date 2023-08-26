from xythrion.bot import Xythrion
from xythrion.extensions.image_generation.gradient_images import GradientImages
from xythrion.extensions.image_generation.gradient_minecraft_skins import (
    GradientMinecraftSkins,
)


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading extensions within this folder."""
    await bot.add_cog(GradientImages(bot))
    await bot.add_cog(GradientMinecraftSkins(bot))
