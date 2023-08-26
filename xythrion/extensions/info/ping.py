from discord.ext.commands import Cog, group

from xythrion.bot import Xythrion
from xythrion.context import Context


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
