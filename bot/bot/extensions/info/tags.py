from discord.ext.commands import Cog, command

from bot.bot import Xythrion
from bot.context import Context


class Tags(Cog):
    """Getting information from tags."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @command()
    async def get_tag(self, ctx: Context, search: str) -> None: ...


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Tags(bot))
