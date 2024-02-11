import re

from bs4 import BeautifulSoup
from discord import Message, utils
from discord.ext.commands import Cog, group
from lxml import etree

from bot.bot import Xythrion
from bot.context import Context
from bot.utils import codeblock, dict_to_human_table, is_trusted

from ._utils.link_converter import DestinationType, validate_destination

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

        # There should only be one channel map per server given there's a successful response
        output_channel_id = channel_maps[0]["output_channel_id"]

        for row in rows:
            if row["from_link"] in message.content:
                new_url: str

                # XOR between to_link and xpath attributes are handled within the API,
                # so we can assume that the data is valid at this point
                if row["to_link"] is not None:
                    new_url = message.content.replace(row["from_link"], row["to_link"])
                else:
                    full_url = self.get_first_url(message.content)
                    webpage = await self.bot.http_client.get(full_url, headers=HEADERS)
                    soup = BeautifulSoup(webpage.content, "html.parser")
                    dom = etree.HTML(str(soup))
                    extracted = dom.xpath(row["xpath"])

                    # "src" for images, "data-src" for videos
                    new_url = extracted[0].get("src") or extracted[0].get("data-src")

                output_channel = utils.get(message.guild.channels, id=output_channel_id)

                await output_channel.send(f"<@{message.author.id}> {message.jump_url} {new_url}")

                break

    @group(aliases=("linkmap", "lm"))
    @is_trusted()
    async def link_map(self, ctx: Context) -> None:
        await ctx.check_subcommands()

    @link_map.group(aliases=("list", "l"))
    @is_trusted()
    async def link_map_list(self, ctx: Context) -> None:
        await ctx.check_subcommands()

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

        if len(data) == 0:
            await ctx.warning_embed("No redirect channels exist.")

            return

        table = dict_to_human_table(data)

        await ctx.send(table)

    @link_map_list.command(name="converters")
    @is_trusted()
    async def list_link_map_converters(self, ctx: Context, attribute: str | None = None) -> None:
        response = await self.bot.api.get(
            "/api/link_maps/converters",
            params={"server_id": ctx.guild.id},
        )

        if not response.is_success:
            await ctx.send(
                f"Something went wrong when requesting link map converters. Status code {response.status_code}.",
            )

            return

        data = response.json()

        if len(data) == 0:
            await ctx.warning_embed("No link converters exist.")

            return

        if attribute is None:
            lst = [
                {
                    "source": x["from_link"],
                    "type": "to_link" if x["to_link"] else "xpath",
                    "destination": x["to_link"] if x["to_link"] else x["xpath"],
                }
                for x in data
            ]
        else:
            lst = [{"source": x["from_link"], attribute: x[attribute]} for x in data]

        table = dict_to_human_table(lst)

        await ctx.send(table)

    @link_map.group(aliases=("create", "c"))
    @is_trusted()
    async def link_map_create(self, ctx: Context) -> None:
        await ctx.check_subcommands()

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

        destination_type = validate_destination(destination)

        match destination_type:
            case DestinationType.XPATH:
                data["xpath"] = destination
            case DestinationType.URL:
                data["to_link"] = destination

        response = await self.bot.api.post("/api/link_maps/converters", data=data)

        data = response.json()

        if not response.is_success:
            await ctx.send(f"Link map creation failed with code {response.status_code}")

            return

        await ctx.send(codeblock(data, language="json"))

    @link_map.group(aliases=("remove", "r"))
    @is_trusted()
    async def link_map_remove(self, ctx: Context) -> None:
        await ctx.check_subcommands()

    @link_map_remove.command(name="converters")
    @is_trusted()
    async def remove_link_map_converter(self, ctx: Context, id: str) -> None:
        response = await self.bot.api.delete(f"/api/link_maps/converters/{id}")

        data = response.json()

        if not response.is_success:
            await ctx.send(f"Link map deletion failed with code {response.status_code}")

            return

        await ctx.send(codeblock(data, language="json"))


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(LinkMapper(bot))
