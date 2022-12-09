from xythrion.bot import Xythrion
from xythrion.extensions.utility.basic import Basic


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading in cogs within this folder."""
    await bot.add_cog(Basic(bot))
