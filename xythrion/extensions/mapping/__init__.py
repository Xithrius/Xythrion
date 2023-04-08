from xythrion.bot import Xythrion
from xythrion.extensions.mapping.links import LinkMapper
from xythrion.extensions.mapping.web import WebMapper


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading extensions within this folder."""
    await bot.add_cog(LinkMapper(bot))
    await bot.add_cog(WebMapper(bot))
