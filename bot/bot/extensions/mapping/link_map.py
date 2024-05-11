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
from tabulate import tabulate  # type: ignore [import-untyped]

from bot.bot import Xythrion
from bot.constants import BS4_HEADERS
from bot.context import Context
from bot.utils import codeblock, is_trusted
from bot.utils.formatting import FAKE_DISCORD_NEWLINE

from ._utils.link_converter import DestinationType, validate_destination

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

    # TODO: Fix return type since `None` should not be possible at this point
    def get_destination(self) -> str | None:
        return self.to_link or self.xpath


class LinkMapper(Cog):
    """Post one link, get another in a better place."""

    def __init__(self, bot: Xythrion):
        self.bot = bot
        self.link_map_channels: list[LinkMapChannel] | None = None

        self.bg_task = self.bot.loop.create_task(self.populate_link_map_channels())

    async def populate_link_map_channels(self) -> None:
        if self.link_map_channels is not None:
            return

        response: Response = await self.bot.api.get("/api/link_maps/channels/all")

        data = response.json()

        self.link_map_channels = [LinkMapChannel(**x) for x in data]

        log.info("Link map channels cache populated")

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

                await output_channel.send(
                    f"<@{message.author.id}> {message.jump_url} {new_url}",
                )

                break

    @group(aliases=("linkmap", "lm"))
    @is_trusted()
    async def link_map(self, ctx: Context) -> None:
        await ctx.check_subcommands()

    @link_map.command(aliases=("summary", "server", "s"))
    async def link_map_server_summary(self, ctx: Context, attribute: str | None = None) -> None:
        if (guild := ctx.guild) is None:
            await ctx.error_embed("Link maps are not supported in DMs")
            return

        show_id = attribute.lower() == "id" if attribute is not None else False

        headers = ("ID", "Source", "Destination") if show_id else ("Source", "Destination")

        # TODO: Reduce code duplication and unecessary if statements
        channels_response: Response = await self.bot.api.get(f"/api/link_maps/server/{guild.id}/channels")
        channels_data = [LinkMapChannel(**x) for x in channels_response.json()]
        channels = (
            [[x.id, x.input_channel_id, x.output_channel_id] for x in channels_data]
            if show_id
            else [[x.input_channel_id, x.output_channel_id] for x in channels_data]
        )
        channels_table = tabulate(channels, headers=headers, maxcolwidths=36)

        converters_response: Response = await self.bot.api.get(f"/api/link_maps/server/{guild.id}/converters")
        converters_data = [LinkMapConverter(**x) for x in converters_response.json()]
        converters = (
            [[x.id, x.from_link, x.get_destination()] for x in converters_data]
            if show_id
            else [[x.from_link, x.get_destination()] for x in converters_data]
        )
        converters_table = tabulate(converters, headers=headers, maxcolwidths=36)

        combined_tables = [
            FAKE_DISCORD_NEWLINE,
            "**Channels**",
            codeblock(channels_table),
            "**Enabled Converters**",
            codeblock(converters_table),
        ]

        content = "\n".join(combined_tables)

        await ctx.send(f"\n{content}")

    @link_map.group(aliases=("list", "l"))
    @is_trusted()
    async def link_map_list(self, ctx: Context) -> None:
        await ctx.check_subcommands()

    @link_map_list.command(aliases=("channel", "channels"))
    @is_trusted()
    async def list_link_map_channels(self, ctx: Context, server_id: int | None = None) -> None:
        if server_id is None and (guild := ctx.guild) is not None:
            server_id = guild.id
        elif guild is None:
            await ctx.error_embed("Link maps are not supported in DMs")
            return

        response: Response = await self.bot.api.get(f"/api/link_maps/server/{server_id}/channels")

        if response.is_error:
            await ctx.error_embed(f"Internal API error: {response.text}")
            return

        data = response.json()

        if not data:
            await ctx.warning_embed("Nothing's here")
            return

        block = codeblock(data, language="json")

        await ctx.send(block)

    @link_map_list.command(aliases=("converter", "converters"))
    @is_trusted()
    async def list_link_map_converters(self, ctx: Context) -> None:
        response: Response = await self.bot.api.get("/api/link_maps/converters/all")

        if response.is_error:
            await ctx.error_embed(f"Internal API error: {response.text}")
            return

        data = response.json()
        block = codeblock(data, language="json")

        await ctx.send(block)

    @link_map.group(aliases=("create", "c"))
    @is_trusted()
    async def link_map_create(self, ctx: Context) -> None:
        await ctx.check_subcommands()

    @link_map_create.command(aliases=("channel", "channels"))
    @is_trusted()
    async def create_link_map_channel(
        self,
        ctx: Context,
        server_id: int,
        input_channel_id: int,
        output_channel_id: int,
    ) -> None:
        payload = {
            "server_id": server_id,
            "input_channel_id": input_channel_id,
            "output_channel_id": output_channel_id,
        }

        response: Response = await self.bot.api.post(
            "/api/link_maps/channels",
            data=payload,
        )

        data = response.json()
        block = codeblock(data, language="json")

        await ctx.send(block)

    @link_map_create.command(aliases=("converter", "converters"))
    @is_trusted()
    async def create_link_map_converter(
        self,
        ctx: Context,
        source: str,
        destination: str,
    ) -> None:
        payload = {
            "from_link": source,
        }

        destination_type = validate_destination(destination)

        match destination_type:
            case DestinationType.XPATH:
                payload["xpath"] = destination
            case DestinationType.URL:
                payload["to_link"] = destination

        response: Response = await self.bot.api.post(
            "/api/link_maps/converters",
            data=payload,
        )

        data = response.json()
        block = codeblock(data, language="json")

        await ctx.send(block)

    @link_map.command(aliases=("enable", "e", "add", "a"))
    @is_trusted()
    async def link_map_converter_enable(self, ctx: Context, channel_id: str, converter_id: str) -> None:
        response: Response = await self.bot.api.put(
            f"/api/link_maps/channels/{channel_id}/converters/{converter_id}",
        )

        await ctx.send(response.status_code)

    @link_map.group(aliases=("remove", "r", "delete", "d"))
    @is_trusted()
    async def link_map_remove(self, ctx: Context) -> None:
        await ctx.check_subcommands()

    @link_map_remove.command(aliases=("channel", "channels"))
    @is_trusted()
    async def remove_link_map_channel(self, ctx: Context, channel_id: str) -> None:
        response: Response = await self.bot.api.delete(
            f"/api/link_maps/channels/{channel_id}",
        )

        data = response.json()
        block = codeblock(data, language="json")

        await ctx.send(block)

    @link_map_remove.command(aliases=("converter", "converters"))
    @is_trusted()
    async def remove_link_map_converter(self, ctx: Context, converter_id: str) -> None:
        response: Response = await self.bot.api.delete(
            f"/api/link_maps/converters/{converter_id}",
        )

        data = response.json()
        block = codeblock(data, language="json")

        await ctx.send(block)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(LinkMapper(bot))
