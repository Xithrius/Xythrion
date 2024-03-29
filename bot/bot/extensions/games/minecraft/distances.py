from math import sqrt

from discord import Embed
from discord.ext.commands import Cog, group

from bot.bot import Xythrion
from bot.context import Context
from bot.utils import str_to_tuple3


class MinecraftDistances(Cog):
    """How far things are from each other in Minecraft."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group()
    async def mc(self, ctx: Context) -> None:
        """Group command for Minecraft distances."""
        await ctx.check_subcommands()

    @mc.command()
    async def distance(
        self,
        ctx: Context,
        start: str,
        end: str,
    ) -> None:
        (x0, y0, z0) = str_to_tuple3(start)
        (x1, y1, z1) = str_to_tuple3(end)

        d: int

        if (x0, y0, z0) == (0, 0, 0):
            d = int(sqrt(x1**2 + y1**2 + z1**2))
        else:
            d = int(sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2 + (z1 - z0) ** 2))

        embed = Embed(
            description=f"`({x0}, {y0}, {z0})` -> `({x1}, {y1}, {z1})` is {int(d)} blocks",
        )

        await ctx.send(embed=embed)

    @mc.command(aliases=("from_overworld",))
    async def to_nether(self, ctx: Context, overworld: str) -> None:
        (x0, y0, z0) = str_to_tuple3(overworld)
        x1, y1, z1 = int(x0 / 8), int(y0 / 8), int(z0 / 8)

        embed = Embed(
            description=f"`overworld ({x0}, {y0}, {z0})` -> `nether ({x1}, {y1}, {z1})`",
        )

        await ctx.send(embed=embed)

    @mc.command(aliases=("from_nether",))
    async def to_overworld(self, ctx: Context, nether: str) -> None:
        (x0, y0, z0) = str_to_tuple3(nether)
        x1, y1, z1 = x0 * 8, y0 * 8, z0 * 8

        embed = Embed(
            description=f"`nether ({x0}, {y0}, {z0})` -> `overworld ({x1}, {y1}, {z1})`",
        )

        await ctx.send(embed=embed)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(MinecraftDistances(bot))
