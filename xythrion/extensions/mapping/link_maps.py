import json

from discord import Message
from discord.ext.commands import Cog, group, is_owner
from httpx import Response

from xythrion.bot import Xythrion
from xythrion.context import Context


class LinkMapper(Cog):
    """Post one link, get replied with another."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @group(aliases=("linkmap",))
    @is_owner()
    async def link_map(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @link_map.command()
    @is_owner()
    async def create_link_map(
        self, ctx: Context, from_match: str, to_match: str
    ) -> None:
        data = {
            "created_at": ctx.message.created_at.replace(tzinfo=None),
            "sid": ctx.guild.id,
            "uid": ctx.author.id,
            "from_match": from_match,
            "to_match": to_match,
        }

        await self.bot.http_client.post(
            "http://localhost:8000/link_map",
            data=json.dumps(data, default=str),
        )

    @link_map.command()
    @is_owner()
    async def get_user_link_maps(self, ctx: Context) -> None:
        data = {"sid": ctx.guild.id, "uid": ctx.author.id}

        r: Response = await self.bot.http_client.get(
            "http://localhost:8000/link_map", params=data
        )

        await ctx.send(r.json())

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        data = {"sid": message.guild.id, "uid": message.author.id}

        r: Response = await self.bot.http_client.get(
            "http://localhost:8000/link_map", params=data
        )

        rows = r.json()

        for row in rows:
            if row["from_match"] in message.content:
                res = message.content.replace(row["from_match"], row["to_match"])

                await message.reply(res)

                break

    # @group()
    # async def link_remap(self, ctx: Context) -> None:
    #     if ctx.invoked_subcommand is None:
    #         await ctx.send("Missing subcommand")

    # @link_remap.group()
    # @is_owner()
    # async def force(self, ctx: Context, from_match: str, to_match: str) -> None:
    #     if ctx.invoked_subcommand is None:
    #         await ctx.send("Missing sub-subcommand")

    # @force.command(aliases=("add",))
    # @is_owner()
    # async def force_add_link_remap(
    #     self, ctx: Context, user: User, from_match: str, to_match: str
    # ) -> None:
    #     if await self.execute_add_remap(ctx.guild.id, user.id, from_match, to_match):
    #         await ctx.send(embed=Embed(description="Link remap added"))
    #     else:
    #         await ctx.send(embed=Embed(description="Link remap already exists"))

    # @force.command(aliases=("remove", "delete"))
    # @is_owner()
    # async def force_remove_link_remap(
    #     self, ctx: Context, user: User, from_match: str
    # ) -> None:
    #     return

    # @link_remapper.command(aliases=("add"))
    # async def add_link_remap(
    #     self, ctx: Context, from_match: str, to_match: str
    # ) -> None:
    #     return

    # @link_remapper.command(aliases=("remove", "delete"))
    # async def remove_link_remap(
    #     self, ctx: Context, from_match: str, to_match: str
    # ) -> None:
    #     return
