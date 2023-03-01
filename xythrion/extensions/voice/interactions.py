from discord.ext.commands import Cog, command


class Interactions(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def tts(self, ctx, *, say: str) -> None:
        """Generates some voice text, offline"""
        await ctx.send(say)
