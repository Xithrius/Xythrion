from discord.ext.commands import Cog, group
from tabulate import tabulate

from bot.bot import Xythrion
from bot.context import Context
from bot.utils import is_trusted
from bot.utils.formatting import codeblock


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
        data = await self.bot.api.get("/v1/docker/containers")

        table = tabulate(data.data, headers="keys")
        block = codeblock(table, language="")

        await ctx.send(block)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Docker(bot))
