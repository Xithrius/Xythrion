from discord import Embed, Message, User
from discord.ext.commands import (
    Cog,
    group,
    is_owner,
)

from xythrion.bot import Xythrion
from xythrion.context import Context


class LinkMapper(Cog):
    """Post one link, get replied with another."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    async def execute_add_remap(
        self, sid: int, uid: int, from_match: str, to_match: str
    ) -> bool:
        async with self.bot.pool.acquire() as conn:
            rows = await conn.execute(
                """
                INSERT INTO link_remaps (
                    sid, uid, from_match, to_match
                ) VALUES ($1, $2, $3, $4)
                """,
                str(sid),
                str(uid),
                from_match,
                to_match,
            )

            return bool(rows)

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        async with self.bot.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM link_remaps WHERE sid = $1 AND uid = $2
                """,
                str(message.guild.id),
                str(message.author.id),
            )

            for row in rows:
                if row["from_match"] in message.content:
                    res = message.content.replace(
                        row["from_match"], row["to_match"]
                    )

                    await message.reply(res)

                    break

    @group()
    async def link_remap(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.reply("Missing subcommand")

    @link_remap.group()
    @is_owner()
    async def force(self, ctx: Context, from_match: str, to_match: str) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.reply("Missing sub-subcommand")

    @force.command(aliases=("add",))
    @is_owner()
    async def force_add_link_remap(
        self, ctx: Context, user: User, from_match: str, to_match: str
    ) -> None:
        if await self.execute_add_remap(
            ctx.guild.id, user.id, from_match, to_match
        ):
            await ctx.reply(embed=Embed(description="Link remap added"))
        else:
            await ctx.reply(
                embed=Embed(description="Link remap already exists")
            )

    @force.command(aliases=("remove", "delete"))
    @is_owner()
    async def force_remove_link_remap(
        self, ctx: Context, user: User, from_match: str
    ) -> None:
        return

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
