from discord.ext.commands import Cog, group

from bot.bot import Xythrion
from bot.context import Context


class Ping(Cog):
    """Pinging different things."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @group()
    async def ping(self, ctx: Context) -> None:
        """Is this thing on?"""
        if ctx.invoked_subcommand is None:
            await ctx.send(":ping_pong: Pong!")

    @ping.command()
    async def api(self, ctx: Context) -> None:
        """Is *that* thing on?"""
        j = await self.bot.api.get("/v1/ping/")

        await ctx.send(j)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Ping(bot))
