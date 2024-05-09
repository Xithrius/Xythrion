import re
from datetime import datetime
from uuid import UUID

import discord
from bs4 import BeautifulSoup
from discord import ChannelType, Message
from discord.ext.commands import Cog, group
from httpx import Response
from loguru import logger as log
from lxml import etree
from pydantic import BaseModel

from bot.bot import Xythrion
from bot.constants import BS4_HEADERS
from bot.context import Context
from bot.utils import is_trusted

REGEX_URL_MATCH = re.compile(r"https?://\S+")


class LinkMapChannel(BaseModel):
    id: UUID
    created_at: datetime
    server_id: int
    input_channel_id: int
    output_channel_id: int


class LinkMapConverter(BaseModel):
    id: UUID
    from_link: str
    to_link: str | None = None
    xpath: str | None = None
    created_at: datetime


class LinkMapper(Cog):
    """Post one link, get another in a better place."""

    def __init__(self, bot: Xythrion):
        self.bot = bot
        self.link_map_channels: list[LinkMapChannel] | None = None

        self.bg_task = self.bot.loop.create_task(self.populate_link_map_channels())

    async def populate_link_map_channels(self) -> None:
        await self.wait_until_ready()

        if self.link_map_channels is not None:
            return

        response: Response = await self.bot.api.get("/api/link_maps/channels/all")

        data = response.json()

        self.link_map_channels = [LinkMapChannel(**x) for x in data]

    def get_link_map_output_channel(self, discord_channel_id: int) -> int | None:
        if (link_map_channels := self.link_map_channels) is not None:
            for link_map_channel in link_map_channels:
                if link_map_channel.input_channel_id == discord_channel_id:
                    return link_map_channel.output_channel_id

        return None

    @staticmethod
    def get_first_url(message: str) -> str | None:
        urls = re.findall(REGEX_URL_MATCH, message)

        return urls[0] if len(urls) else None

    async def extract_url_from_webpage(self, url: str, xpath: str) -> str:
        webpage = await self.bot.http_client.get(url, headers=BS4_HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        dom = etree.HTML(str(soup), None)
        extracted = dom.xpath(xpath)

        # "src" for images, "data-src" for videos
        extracted_url = extracted[0].get("src") or extracted[0].get("data-src")

        return extracted_url

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.guild is None or message.author.bot:
            return

        channel_id = message.channel.id

        if (output_channel_id := self.get_link_map_output_channel(channel_id)) is None:
            return

        response: Response = await self.bot.api.get(
            f"/api/link_maps/channels/{channel_id}/converters",
        )

        data = response.json()

        converters = [LinkMapConverter(**x) for x in data]

        # Hopefully this branch does not get hit
        if not response.is_success:
            log.error(
                f"Discord channel ID '{channel_id}' missed on getting link map converter(s). "
                "This is cache invalidation! Was a link map converter or channel not created/deleted properly?",
            )
            return

        if (output_channel := discord.utils.get(message.guild.channels, id=output_channel_id)) is None:
            log.error(f"Could not retrieve channel {output_channel_id} for link map")
            return

        if output_channel.type != ChannelType.text:
            log.error(f"Link map output channel {output_channel_id} is not a text channel")
            return

        for converter in converters:
            if converter.from_link in message.content:
                new_url: str

                if (to_link := converter.to_link) is not None:
                    new_url = message.content.replace(converter.from_link, to_link)
                elif (xpath := converter.xpath) is not None:
                    if (full_url := self.get_first_url(message.content)) is None:
                        log.error(f"Could not extract any links from {message.jump_url} for link converter")

                        return

                    new_url = await self.extract_url_from_webpage(full_url, xpath)

                # TODO: Fix this line so the channel is the correct type
                await output_channel.send(
                    f"<@{message.author.id}> {message.jump_url} {new_url}",
                )

                break

    @group(aliases=("linkmap", "lm"))
    @is_trusted()
    async def link_map(self, ctx: Context) -> None:
        await ctx.check_subcommands()

    @link_map.group(aliases=("list", "l"))
    @is_trusted()
    async def link_map_list(self, ctx: Context) -> None:
        await ctx.check_subcommands()

    @link_map_list.command(name="channel")
    @is_trusted()
    async def list_link_map_channels(self, ctx: Context) -> None: ...

    @link_map_list.command(name="converter")
    @is_trusted()
    async def list_link_map_converters(
        self,
        ctx: Context,
        input_channel_id: str | None = None,
        attribute: str | None = None,
    ) -> None: ...

    @link_map.group(aliases=("create", "c"))
    @is_trusted()
    async def link_map_create(self, ctx: Context) -> None:
        await ctx.check_subcommands()

    @link_map_create.command(name="channel")
    @is_trusted()
    async def create_link_map_channel(
        self,
        ctx: Context,
        input_channel_id: int,
        output_channel_id: int,
    ) -> None: ...

    @link_map_create.command(name="converter")
    @is_trusted()
    async def create_link_map_converter(
        self,
        ctx: Context,
        source: str,
        destination: str,
    ) -> None: ...

    @link_map.command(aliases=("enable", "e", "add", "a"))
    @is_trusted()
    async def link_map_converter_enable(self, ctx: Context) -> None: ...

    @link_map.group(aliases=("remove", "r", "delete", "d"))
    @is_trusted()
    async def link_map_remove(self, ctx: Context) -> None:
        await ctx.check_subcommands()

    @link_map_remove.command(name="channel")
    @is_trusted()
    async def remove_link_map_channel(self, ctx: Context, converter_id: str) -> None: ...

    @link_map_remove.command(name="converter")
    @is_trusted()
    async def remove_link_map_converter(self, ctx: Context, converter_id: str) -> None: ...


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(LinkMapper(bot))
