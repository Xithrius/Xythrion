from discord.ext.commands import Cog, command

from bot.bot import Xythrion
from bot.context import Context


class VoiceChannelInteractions(Cog):
    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command()
    async def join(self, ctx: Context) -> None:
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
        else:
            await ctx.send("You are not in a voice channel.")
            return

        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)

            return

        await channel.connect()

    @command()
    async def leave(self, ctx: Context) -> None:
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

            return

        await ctx.send("I am not in a voice channel")


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(VoiceChannelInteractions(bot))
