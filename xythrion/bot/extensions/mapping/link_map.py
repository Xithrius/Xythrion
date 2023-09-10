from discord import Message
from discord.ext.commands import Cog, group

from bot.bot import Xythrion
from bot.context import Context


class LinkMapper(Cog):
    """Post one link, get replied with another."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        data = {"sid": message.guild.id, "uid": message.author.id}

        rows = await self.bot.api.get("/v1/link_map/", params=data)

        for row in rows:
            if row["from_match"] in message.content:
                res = message.content.replace(row["from_match"], row["to_match"])

                await message.reply(res)

                break

    @group(aliases=("linkmap",))
    async def link_map(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @link_map.command()
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

        await self.bot.api.post("/v1/link_map/", data=data)

    @link_map.command()
    async def get_user_link_maps(self, ctx: Context) -> None:
        data = {"sid": ctx.guild.id, "uid": ctx.author.id}

        j = await self.bot.api.get("/v1/link_map/", params=data)

        await ctx.send(j)

    @link_map.command()
    async def remove_user_link_map(self, ctx: Context, id: int) -> None:
        j = await self.bot.api.delete(f"/v1/link_map/{id}")

        await ctx.send(j)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(LinkMapper(bot))
