from dataclasses import dataclass
from datetime import datetime

from discord.ext.commands import Cog, group, is_owner
from httpx import Response

from bot.bot import Xythrion
from bot.context import Context
from bot.utils import dict_to_human_table


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
        await ctx.check_subcommands()

    @trust.command(aliases=("list",))
    @is_owner()
    async def list_trusted(self, ctx: Context) -> None:
        r: Response = await self.bot.api.get("/api/trusted/")

        if data := r.json():
            table = dict_to_human_table(data, datetime_key="at")

            await ctx.send(table)

            return

        await ctx.send("No one is trusted at this moment.")

    @trust.command(aliases=("add",))
    @is_owner()
    async def add_trust(self, ctx: Context, user_id: int) -> None:
        response: Response = await self.bot.api.post(
            "/api/trusted/",
            data={"user_id": user_id},
        )

        if not response.is_success:
            await ctx.send("Trust for this user already exists")

            return

        data = response.json()

        await ctx.send(f"Trust given to <@{user_id}> at {data['at']}")

    @trust.command(aliases=("remove", "delete"))
    @is_owner()
    async def remove_trust(self, ctx: Context, user_id: int) -> None:
        await self.bot.api.delete(f"/api/trusted/{user_id}")

        await ctx.send(f"Trust removed from <@{user_id}>")


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Trusted(bot))
