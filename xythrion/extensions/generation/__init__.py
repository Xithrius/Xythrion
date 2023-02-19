from xythrion.bot import Xythrion
from xythrion.extensions.generation.expr import GraphExpression
from xythrion.extensions.generation.rand import GraphRandom


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading extensions within this folder."""
    await bot.add_cog(GraphExpression(bot))
    await bot.add_cog(GraphRandom(bot))
