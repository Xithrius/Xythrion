import re

from bs4 import BeautifulSoup
from discord import Message
from discord.ext.commands import Cog, group
from lxml import etree

from bot.bot import Xythrion
from bot.context import Context

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
}
REGEX_URL_MATCH = re.compile(r"https?://\S+")


class WebMapper(Cog):
    """Retrieve an XPATH from a website."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @staticmethod
    def get_first_url(message: str) -> str | None:
        urls = re.findall(REGEX_URL_MATCH, message)

        return urls[0] if len(urls) else None

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        data = {"sid": message.guild.id, "uid": message.author.id}

        rows = await self.bot.api.get("/v1/web_map/", params=data)

        for row in rows:
            if row["matches"] in message.content:
                full_url = self.get_first_url(message.content)
                webpage = await self.bot.api.http_client.get(full_url, headers=HEADERS)
                soup = BeautifulSoup(webpage.content, "html.parser")
                dom = etree.HTML(str(soup))
                extracted = dom.xpath(row["xpath"])
                xpath_url_extract = extracted[0].get("data-src")

                await message.reply(xpath_url_extract)

                break

    @group(aliases=("webmap",))
    async def web_map(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @web_map.command()
    async def create_web_map(self, ctx: Context, matches: str, xpath: str) -> None:
        data = {
            "sid": ctx.guild.id,
            "uid": ctx.author.id,
            "created_at": ctx.message.created_at.replace(tzinfo=None),
            "matches": matches,
            "xpath": xpath,
        }

        await self.bot.api.post("/v1/web_map/", data=data)

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
