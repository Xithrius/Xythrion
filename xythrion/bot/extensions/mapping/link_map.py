import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from discord import Message, utils
from discord.ext.commands import Cog, group
from lxml import etree

from bot.bot import Xythrion
from bot.context import Context
from bot.utils import codeblock, dict_to_human_table, is_trusted

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
}
REGEX_URL_MATCH = re.compile(r"https?://\S+")


class LinkMapper(Cog):
    """Post one link, get another in a better place."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @staticmethod
    def get_first_url(message: str) -> str | None:
        urls = re.findall(REGEX_URL_MATCH, message)

        return urls[0] if len(urls) else None

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.guild is None or message.author.id == self.bot.user.id:
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

        rows = response.json()

        response = await self.bot.api.get(
            "/api/link_maps/channels",
            params={"server_id": message.guild.id},
        )

        if not response.is_success:
            return

        channel_maps = response.json()

        # There should only be one channel map per server
        output_channel_id = channel_maps[0]["output_channel_id"]

        for row in rows:
            if row["from_link"] in message.content:
                new_url: str

                if row["to_link"] is not None:
                    new_url = message.content.replace(row["from_link"], row["to_link"])
                else:
                    full_url = self.get_first_url(message.content)
                    webpage = await self.bot.http_client.get(full_url, headers=HEADERS)
                    soup = BeautifulSoup(webpage.content, "html.parser")
                    dom = etree.HTML(str(soup))
                    extracted = dom.xpath(row["xpath"])
                    xpath_url_extract = extracted[0].get("src") or extracted[0].get("data-src")

                    new_url = xpath_url_extract

                output_channel = utils.get(message.guild.channels, id=output_channel_id)

                await output_channel.send(f"<@{message.author.id}> {message.jump_url} {new_url}")

                break

    @group(aliases=("linkmap", "lm"))
    @is_trusted()
    async def link_map(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @link_map.group(aliases=("list", "l"))
    @is_trusted()
    async def link_map_list(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @link_map_list.command(name="channels")
    @is_trusted()
    async def list_link_map_channels(self, ctx: Context) -> None:
        response = await self.bot.api.get("/api/link_maps/channels")

        if not response.is_success:
            await ctx.send(
                f"Something went wrong when requesting link map channels. Status code {response.status_code}.",
            )

            return

        data = response.json()

        table = dict_to_human_table(data)

        await ctx.send(table)

    @link_map_list.command(name="converters")
    @is_trusted()
    async def list_link_map_converters(self, ctx: Context) -> None:
        response = await self.bot.api.get("/api/link_maps/converters")

        if not response.is_success:
            await ctx.send(
                f"Something went wrong when requesting link map converters. Status code {response.status_code}.",
            )

            return

        data = [
            {"source": x["from_link"], "destination": x["to_link"] if x["to_link"] else x["xpath"]}
            for x in response.json()
        ]

        table = dict_to_human_table(data)

        await ctx.send(table)

    @link_map.group(aliases=("create", "c"))
    @is_trusted()
    async def link_map_create(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @link_map_create.command(name="channels")
    @is_trusted()
    async def create_link_map_channel(
        self,
        ctx: Context,
        input_channel_id: int,
        output_channel_id: int,
    ) -> None:
        data = {
            "server_id": ctx.guild.id,
            "input_channel_id": input_channel_id,
            "output_channel_id": output_channel_id,
        }

        response = await self.bot.api.post("/api/link_maps/channels", data=data)

        if not response.is_success:
            if response.status_code == 409:
                await ctx.send("Link map channel redirection already exists.")
            else:
                await ctx.send(f"Link map channel redirection failed with code {response.status_code}")

            return

        await ctx.send(f"Link map channel redirection created: <#{input_channel_id}> -> <#{output_channel_id}>")

    @link_map_create.command(name="converters")
    @is_trusted()
    async def create_link_map_converter(
        self,
        ctx: Context,
        source: str,
        destination: str,
    ) -> None:
        data = {
            "channel_map_server_id": ctx.guild.id,
            "from_link": source,
        }

        try:
            urlparse(destination)
            data["to_link"] = destination
        except ValueError:
            data["xpath"] = destination

        response = await self.bot.api.post("/api/link_maps/converters", data=data)

        data = response.json()

        if not response.is_success:
            await ctx.send(f"Link map creation failed with code {response.status_code}")

            return

        await ctx.send(codeblock(data, language="json"))


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(LinkMapper(bot))
