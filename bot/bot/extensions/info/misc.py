from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog, command
from humanize import naturaldelta

from bot.bot import Xythrion
from bot.context import Context


class Misc(Cog):
    def __init__(self, bot: Xythrion):
        self.bot = bot

    @command(name="prefix")
    async def get_prefix(self, ctx: Context) -> None:
        embed = Embed(description=self.bot.command_prefix_str)

        await ctx.send(embed=embed)

    @command(name="uptime")
    async def get_uptime(self, ctx: Context) -> None:
        current_datetime = datetime.now(self.bot.tzinfo)

        if (bot_startup_datetime := self.bot.startup_datetime) is None:
            await ctx.error_embed("The bot has not fully started up yet, please try again later")
            return

        delta = current_datetime - bot_startup_datetime
        human_delta = naturaldelta(delta.total_seconds())

        await ctx.send(human_delta)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Misc(bot))
