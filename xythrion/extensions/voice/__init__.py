from xythrion.bot import Xythrion
from xythrion.extensions.voice.interactions import Interactions
from xythrion.extensions.voice.streaming import Streaming


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading extensions within this folder."""
    await bot.add_cog(Interactions(bot))
    await bot.add_cog(Streaming(bot))
