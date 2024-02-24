from discord import Embed
from discord.ext.commands import Cog, command

from bot.bot import Xythrion
from bot.context import Context


class Misc(Cog):
    def __init__(self, bot: Xythrion):
        self.bot = bot

    @command()
    async def get_prefix(self, ctx: Context) -> None:
        embed = Embed(description=self.bot.command_prefix_str)

        await ctx.send(embed=embed)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Misc(bot))
