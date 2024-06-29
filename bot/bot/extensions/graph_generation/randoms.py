from io import BytesIO
from random import randint

import pandas as pd
from discord.ext.commands import Cog, command

from bot.bot import Xythrion
from bot.context import Context
from bot.utils.plotting import plot_generic_2d


class RandomGraphGeneration(Cog):
    """Graph random data."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @staticmethod
    async def __plot_histogram_2d(df: pd.DataFrame, rolls: int) -> BytesIO:
        return await plot_generic_2d(
            df,
            plot_type="histogram",
            title=f"Histogram of {rolls} rolls of dice",
            x_label="value",
            y_label="amount",
        )

    @command(aliases=("roll",))
    async def dice(self, ctx: Context, rolls: int = 10) -> None:
        """Rolls a die anywhere between 1 and 10 times."""
        if rolls < 10 or rolls > 100:
            await ctx.error_embed("Amount of rolls must be between 10 and 100.")
            return

        df = pd.DataFrame([randint(1, 6) for _ in range(rolls)], columns=["value"])

        b = await self.__plot_histogram_2d(df, rolls)

        await ctx.send_image_buffer(b)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(RandomGraphGeneration(bot))
