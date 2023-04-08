from discord.ext.commands import Cog, command

from xythrion.bot import Xythrion
from xythrion.context import Context


class Ping(Cog):
    """Pinging the bot, to see if it's alive."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @command()
    async def ping(self, ctx: Context) -> None:
        """Is this thing on?"""
        await ctx.reply(":ping_pong: Pong!")

    @command()
    async def ping_api(self, ctx: Context) -> None:
        """Is *that* thing on?"""
        r = await self.bot.http_client.get("http://localhost:8000/ping")

        await ctx.send(r.json())
