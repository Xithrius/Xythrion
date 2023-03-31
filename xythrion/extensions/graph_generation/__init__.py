from xythrion.bot import Xythrion
from xythrion.extensions.graph_generation.expressions import GraphExpression
from xythrion.extensions.graph_generation.randoms import GraphRandom


async def setup(bot: Xythrion) -> None:
    """The necessary function for loading extensions within this folder."""
    await bot.add_cog(GraphExpression(bot))
    await bot.add_cog(GraphRandom(bot))
