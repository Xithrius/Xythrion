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
        r: Response = await self.bot.internal_api_client.get("/api/trusted/")

        if data := r.json():
            table = dict_to_human_table(data)

            await ctx.send(table)

            return

        await ctx.send("No one is trusted at this moment.")

    @trust.command(aliases=("add",))
    @is_owner()
    async def add_trust(self, ctx: Context, user_id: int) -> None:
        response: Response = await self.bot.internal_api_client.post(
            "/api/trusted/",
            data={"user_id": user_id},
        )

        if response.status_code == 409:
            await ctx.warning_embed("Trust for this user already exists")
            return
        if response.is_error:
            await ctx.error_embed(f"Error when trusting user: {response.status_code} - {response.text}")
            return

        data = response.json()

        await ctx.send(f"Trust given to <@{user_id}> at {data["at"]}")

    @trust.command(aliases=("remove", "delete"))
    @is_owner()
    async def remove_trust(self, ctx: Context, user_id: int) -> None:
        await self.bot.internal_api_client.delete(f"/api/trusted/{user_id}")

        await ctx.done()


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Trusted(bot))
