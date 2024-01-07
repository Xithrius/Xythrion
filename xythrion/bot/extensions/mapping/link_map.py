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
    created_at: datetime
    from_link: str
    to_link: str


class LinkMapper(Cog):
    """Post one link, get replied with another."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.guild is None:
            return

        response = await self.bot.api.get(
            "/api/link_maps/converters",
            params={
                "server_id": message.guild.id,
                "input_channel_id": message.channel.id,
            },
        )

        if not response.is_success:
            return

        rows: list[LinkMapData] = response.json()

        for row in rows:
            if row.from_link in message.content:
                res = message.content.replace(row.from_link, row.to_link)

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

        await self.bot.api.post("/api/link_maps/", data=data)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(LinkMapper(bot))
