from dataclasses import dataclass
from datetime import datetime

from discord import Message
from discord.ext.commands import Cog, group

from bot.bot import Xythrion
from bot.context import Context


@dataclass
class LinkMapData:
    id: int
    server_id: int
    user_id: int
    created_at: datetime
    from_match: str
    to_match: str


class LinkMapper(Cog):
    """Post one link, get replied with another."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.guild is None:
            return

        data = {"server_id": message.guild.id, "user_id": message.author.id}

        response = await self.bot.api.get("/v1/link_maps/", params=data)

        rows: list[LinkMapData] = response.data

        for row in rows:
            if row.from_match in message.content:
                res = message.content.replace(row.from_match, row.to_match)

                await message.reply(res)

                break

    @group(aliases=("linkmap",))
    async def link_map(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @link_map.command()
    async def create_link_map(
        self,
        ctx: Context,
        from_match: str,
        to_match: str,
        guild_id: int | None = None,
    ) -> None:
        data = {
            "created_at": ctx.message.created_at.replace(tzinfo=None),
            "user_id": ctx.author.id,
            "from_match": from_match,
            "to_match": to_match,
        }

        if guild_id is not None:
            data["server_id"] = guild_id
        elif ctx.guild is not None:
            data["server_id"] = ctx.guild.id
        else:
            await ctx.send(
                "Command sent was not in guild channel, and no guild channel specified.",
            )

            return

        await self.bot.api.post("/v1/link_maps/", data=data)

    @link_map.command()
    async def get_user_link_maps(self, ctx: Context) -> None:
        data = {"server_id": ctx.guild.id, "user_id": ctx.author.id}

        j = await self.bot.api.get("/v1/link_maps/", params=data)

        await ctx.send(j)

    @link_map.command()
    async def remove_user_link_map(self, ctx: Context, id: int) -> None:
        j = await self.bot.api.delete(f"/v1/link_maps/{id}")

        await ctx.send(j)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(LinkMapper(bot))
