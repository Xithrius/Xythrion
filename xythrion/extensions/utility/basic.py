from disnake.ext.commands import Cog, Context, command

from xythrion.bot import Xythrion


class Basic(Cog):
    """Just some simple commands of a utility type."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @command()
    async def ping(self, ctx: Context) -> None:
        """A basic command to make sure that the bot is working."""
        await ctx.reply(":ping_pong: Pong!")
