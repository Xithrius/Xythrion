from xythrion.bot import Xythrion
from xythrion.extensions.space.mars_weather import MarsWeather


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading extensions within this folder."""
    await bot.add_cog(MarsWeather(bot))
