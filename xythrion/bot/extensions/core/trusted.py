from dataclasses import dataclass
from datetime import datetime

from discord.ext.commands import Cog, group, is_owner

from bot.api import InternalAPIResponse
from bot.bot import Xythrion
from bot.context import Context


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
        data: list[TrustedData] = await self.bot.api.get("/v1/trusted/")

        await ctx.send(data)

    @trust.command(aliases=("add",))
    @is_owner()
    async def add_trust(self, ctx: Context, user_id: int) -> None:
        data: InternalAPIResponse = await self.bot.api.post(
            "/v1/trusted/", data={"user_id": int(user_id)}
        )

        # await ctx.send(f"Trust given to <@{user_id}> at {data.data['at']}")
        await ctx.send(data.data)

    @trust.command(aliases=("remove", "delete"))
    @is_owner()
    async def remove_trust(self, ctx: Context, user_id: int) -> None:
        await self.bot.api.delete(f"/v1/trusted/{user_id}")

        await ctx.send(f"Trust removed from <@{user_id}>")


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Trusted(bot))
