import json

from bot.context import Context
from bs4 import BeautifulSoup
from discord import Message
from discord.ext.commands import Cog, group
from lxml import etree

from bot.bot import Xythrion

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
}


class WebMapper(Cog):
    """Retrieve an XPATH from a website."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        data = {"sid": message.guild.id, "uid": message.author.id}

        rows = await self.bot.api.get("/v1/web_map/", params=data)

        for row in rows:
            if row["matches"] in message.content:
                # res = message.content.replace(row["from_match"], row["to_match"])
                webpage = self.bot.api.http_client.get(message.content, headers=HEADERS)

                # webpage = self.bot.api.request(argv[1], headers=HEADERS)
                soup = BeautifulSoup(webpage.content, "html.parser")
                dom = etree.HTML(str(soup))

                x = dom.xpath(row["xpath"])
                await message.reply(x)

                break

    @group(aliases=("webmap",))
    async def web_map(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @web_map.command()
    async def create_web_map(
        self, ctx: Context, from_match: str, to_match: str
    ) -> None:
        data = {
            "sid": ctx.guild.id,
            "uid": ctx.author.id,
            "created_at": ctx.message.created_at.replace(tzinfo=None),
            "matches": from_match,
            "xpath": to_match,
        }

        await self.bot.api.post(
            "/v1/web_map/",
            data=json.dumps(data, default=str),
        )

    @web_map.command()
    async def get_user_web_maps(self, ctx: Context) -> None:
        data = {"sid": ctx.guild.id, "uid": ctx.author.id}

        j = await self.bot.api.get("/v1/web_map/", params=data)

        await ctx.send(j)

    @web_map.command()
    async def remove_user_web_map(self, ctx: Context, id: int) -> None:
        j = await self.bot.api.delete(f"/v1/web_map/{id}")

        await ctx.send(j)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(WebMapper(bot))
