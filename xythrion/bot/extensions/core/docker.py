from discord.ext.commands import Cog, group

from bot.bot import Xythrion
from bot.context import Context
from bot.utils import dict_to_human_table, is_trusted


class Docker(Cog):
    """Observing docker containers."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group()
    @is_trusted()
    async def docker(self, ctx: Context) -> None:
        """Docker group command."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @docker.command(aliases=("ps", "containers"))
    @is_trusted()
    async def list_containers(self, ctx: Context) -> None:
        data = await self.bot.api.get("/api/docker/containers")

        table = dict_to_human_table(data.data, datetime_key="created")

        await ctx.send(table)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Docker(bot))
