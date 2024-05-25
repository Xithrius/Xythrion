import re
from enum import Enum

import pandas as pd
from discord.ext.commands import Cog, command

from bot.bot import Xythrion
from bot.context import Context
from bot.utils import is_trusted
from bot.utils.plotting.scatter import plot_scatter_2d

MULTIPOINT_2D_REGEX = re.compile(r"\((\d+),(\d+)(?:,\s*\d+)?\)")
MULTIPOINT_3D_REGEX = re.compile(r"\((\d+),(\d+),(\d+)(?:,\s*\d+)?\)")


class MultiPointType(Enum):
    DOUBLE = 1
    TRIPLE = 2


def extract_points(s: str) -> tuple[MultiPointType, list[tuple[str, str] | tuple[str, str, str]]]:
    if points_3d := re.findall(MULTIPOINT_3D_REGEX, s):
        return MultiPointType.TRIPLE, points_3d
    if points_2d := re.findall(MULTIPOINT_2D_REGEX, s):
        return MultiPointType.DOUBLE, points_2d

    raise ValueError("Input contains both 2D and 3D points.")


class ManualGraphGeneration(Cog):
    """Graphing points given by users."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command()
    @is_trusted()
    async def manual_graph(self, ctx: Context, points: str) -> None:
        point_type, matches = extract_points(points)

        point_arr = [[int(y) for y in match] for match in matches]
        df = pd.DataFrame(point_arr, columns=["x", "y"] if point_type == MultiPointType.DOUBLE else ["x", "y", "z"])
        await plot_scatter_2d(df, ctx=ctx)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(ManualGraphGeneration(bot))
