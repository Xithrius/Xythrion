import asyncio
from datetime import datetime

import discord
from discord import Embed
from discord.ext.commands import Cog, command
from humanize import naturaldelta
from loguru import logger as log

from bot.bot import Xythrion
from bot.context import Context
from bot.settings import settings


class Misc(Cog):
    def __init__(self, bot: Xythrion):
        self.bot = bot

        self.bg_presence_uptime_task = self.bot.loop.create_task(self.presence_uptime_task())

    async def presence_uptime_task(self) -> None:
        await self.bot.wait_until_ready()
        log.info("Started presence uptime background task")

        while not self.bot.is_closed():
            current_datetime = datetime.now(self.bot.tzinfo)
            delta = current_datetime - (self.bot.startup_datetime or current_datetime)
            human_delta = naturaldelta(delta.total_seconds())

            presence = discord.CustomActivity(f"Up for {human_delta}")
            await self.bot.change_presence(activity=presence)

            await asyncio.sleep(60)

    @command(name="prefix")
    async def get_prefix(self, ctx: Context) -> None:
        embed = Embed(description=settings.prefix)

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
