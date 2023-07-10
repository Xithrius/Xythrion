from discord.ext.commands import (
    Cog,
    group,
)

from xythrion.bot import Xythrion
from xythrion.context import Context


class LinkMapper(Cog):
    """Post one link, get replied with another."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @group(aliases=("linkmap",))
    async def link_map(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @link_map.command()
    async def create_link_map(self, ctx: Context) -> None:
        await self.bot.http_client.post(
            "http://localhost:8000/link_map",
            json={
                "sid": ctx.guild.id,
                "uid": ctx.author.id,
                "from_match": "asdf",
                "to_match": "fdsa",
            },
        )

    # async def execute_add_remap(
    #     self, sid: int, uid: int, from_match: str, to_match: str
    # ) -> bool:
    #     async with self.bot.pool.acquire() as conn:
    #         rows = await conn.execute(
    #             """
    #             INSERT INTO link_remaps (
    #                 sid, uid, from_match, to_match
    #             ) VALUES ($1, $2, $3, $4)
    #             """,
    #             str(sid),
    #             str(uid),
    #             from_match,
    #             to_match,
    #         )

    #         return bool(rows)

    # @Cog.listener()
    # async def on_message(self, message: Message) -> None:
    #     async with self.bot.pool.acquire() as conn:
    #         rows = await conn.fetch(
    #             """
    #             SELECT * FROM link_remaps WHERE sid = $1 AND uid = $2
    #             """,
    #             str(message.guild.id),
    #             str(message.author.id),
    #         )

    #         for row in rows:
    #             if row["from_match"] in message.content:
    #                 res = message.content.replace(row["from_match"], row["to_match"])

    #                 await message.reply(res)

    #                 break

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
