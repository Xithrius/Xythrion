from math import sqrt

from bot.context import Context
from bot.utils import convert_3d_tuples
from discord import Embed
from discord.ext.commands import Cog, group

from bot.bot import Xythrion


class MinecraftDistances(Cog):
    """How far things are from each other in Minecraft."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group()
    async def mc(self, ctx: Context) -> None:
        """Group command for Minecraft distances."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @mc.command()
    async def distance(
        self, ctx: Context, start: convert_3d_tuples, end: convert_3d_tuples
    ) -> None:
        (x0, y0, z0), (x1, y1, z1) = start, end

        d: int

        if (x0, y0, z0) == (0, 0, 0):
            d = sqrt(x1**2 + y1**2 + z1**2)
        else:
            d = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2 + (z1 - z0) ** 2)

        embed = Embed(
            description=f"`({x0}, {y0}, {z0})` -> `({x1}, {y1}, {z1})` is {int(d)} blocks"
        )

        await ctx.send(embed=embed)

    @mc.command(aliases=("from_overworld",))
    async def to_nether(self, ctx: Context, overworld: convert_3d_tuples) -> None:
        (x0, y0, z0) = overworld
        x1, y1, z1 = int(x0 / 8), int(y0 / 8), int(z0 / 8)

        embed = Embed(
            description=f"`overworld ({x0}, {y0}, {z0})` -> `nether ({x1}, {y1}, {z1})`"
        )

        await ctx.send(embed=embed)

    @mc.command(aliases=("from_nether",))
    async def to_overworld(self, ctx: Context, nether: convert_3d_tuples) -> None:
        (x0, y0, z0) = nether
        x1, y1, z1 = x0 * 8, y0 * 8, z0 * 8

        embed = Embed(
            description=f"`nether ({x0}, {y0}, {z0})` -> `overworld ({x1}, {y1}, {z1})`"
        )

        await ctx.send(embed=embed)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(MinecraftDistances(bot))
