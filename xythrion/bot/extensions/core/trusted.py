from dataclasses import dataclass
from datetime import datetime

from discord.ext.commands import Cog, group, is_owner
from tabulate import tabulate

from bot.api import InternalAPIResponse
from bot.bot import Xythrion
from bot.context import Context
from bot.utils import codeblock, convert_to_deltas


@dataclass
class TrustedData:
    id: int
    user_id: int
    at: datetime


class Trusted(Cog):
    """Adding trusted users for elevated commands."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group(aliases=("trusted",))
    @is_owner()
    async def trust(self, ctx: Context) -> None:
        """Trust group command."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @trust.command(aliases=("list",))
    @is_owner()
    async def list_trusted(self, ctx: Context) -> None:
        data: InternalAPIResponse = await self.bot.api.get("/v1/trusted/")

        data.data = convert_to_deltas(data.data, "at")

        table = tabulate(data.data, headers="keys")
        block = codeblock(table)

        await ctx.send(block)

    @trust.command(aliases=("add",))
    @is_owner()
    async def add_trust(self, ctx: Context, user_id: int) -> None:
        data: InternalAPIResponse = await self.bot.api.post(
            "/v1/trusted/", data={"user_id": user_id}
        )

        if data.status != 201:
            await ctx.send("Trust for this user already exists")

            return

        await ctx.send(f"Trust given to <@{user_id}> at {data.data['at']}")

    @trust.command(aliases=("remove", "delete"))
    @is_owner()
    async def remove_trust(self, ctx: Context, user_id: int) -> None:
        await self.bot.api.delete(f"/v1/trusted/{user_id}")

        await ctx.send(f"Trust removed from <@{user_id}>")


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Trusted(bot))
