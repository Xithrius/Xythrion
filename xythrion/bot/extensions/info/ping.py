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
        await ctx.check_subcommands()


    @ping.command()
    async def api(self, ctx: Context) -> None:
        """Is *that* thing on?"""
        response = await self.bot.api.get("/api/health")

        await ctx.send("API is healthy" if response.is_success else "API is unhealthy")

    @ping.command(aliases=("discord",))
    async def latency(self, ctx: Context) -> None:
        await ctx.send(f"Latency: {self.bot.latency*1000:.0f}ms")


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Ping(bot))
