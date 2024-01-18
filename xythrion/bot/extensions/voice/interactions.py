from discord import Member, VoiceState
from discord.ext.commands import Cog, command
from loguru import logger as log

from bot.bot import Xythrion
from bot.context import Context


class VoiceChannelInteractions(Cog):
    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState) -> None:
        bot_voice_channel = None
        for vc in self.bot.voice_clients:
            if vc.guild == member.guild:
                bot_voice_channel = vc.channel
                break

        if not bot_voice_channel:
            return

        # Check if a user joins the voice channel the bot is in
        if after.channel == bot_voice_channel and member != self.bot.user:
            log.info(f"{member} joined the voice channel {after.channel.name}.")

        # Check if a user leaves the voice channel the bot is in
        if before.channel == bot_voice_channel and after.channel != bot_voice_channel:
            log.info(f"{member} left the voice channel {before.channel.name}.")

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
