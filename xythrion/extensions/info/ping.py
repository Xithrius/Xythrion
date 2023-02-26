from discord.ext.commands import Cog, Context, command
import httpx

from xythrion.bot import Xythrion


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
        res = httpx.get("localhost:8000/ping")

        j = res.json()

        print(j)
