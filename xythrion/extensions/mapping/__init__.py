from xythrion.bot import Xythrion
from xythrion.extensions.mapping.link_maps import LinkMapper


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading extensions within this folder."""
    await bot.add_cog(LinkMapper(bot))
