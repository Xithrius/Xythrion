from collections import Counter
from random import randint

import pandas as pd
from discord import Embed
from discord.ext.commands import Cog, command

from bot.bot import Xythrion
from bot.context import Context


class GraphRandom(Cog):
    """Graph random data."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    # TODO: Create a generic bar plot so dataframe data can be shown properly
    @command(aliases=("roll",), enabled=False)
    async def dice(self, ctx: Context, rolls: int = 1) -> None:
        """Rolls a die anywhere between 1 and 10 times."""
        if rolls not in range(1, 11):
            embed = Embed(description="Amount of rolls must be between 1 and 10.")

            await ctx.send(embed=embed)

            return

        counts = Counter(randint(1, 6) for _ in range(rolls))

        df = pd.DataFrame(
            [[i, counts[i]] for i in range(1, 7)],
            columns=("roll", "amount"),
        )

        await ctx.send(df.to_string())

        # buffer = await graph_2d(
        #     df["roll"], df["amount"], graph_type="bar", autorotate_xaxis=False
        # )

        # embed = Embed(
        #     description=f"Graph of {rolls} dice roll{'s' if rolls > 1 else ''}."
        # )

        # await send_image_buffer(buffer, ctx=ctx, embed=embed)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(GraphRandom(bot))
