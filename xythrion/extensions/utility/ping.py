from discord.ext.commands import Cog, Context, command

from xythrion.bot import Xythrion


class Ping(Cog):
    """Pinging the bot, to see if it's alive."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @command()
    async def ping(self, ctx: Context) -> None:
        """Is this thing on?"""
        await ctx.reply(":ping_pong: Pong!")
