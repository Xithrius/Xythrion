from dataclasses import dataclass
from datetime import datetime

from discord import Message
from discord.ext.commands import Cog, group

from bot.bot import Xythrion
from bot.context import Context
from bot.utils import is_trusted


@dataclass
class LinkMapData:
    id: int
    server_id: int
    created_at: datetime
    from_link: str
    to_link: str
    xpath: str | None = None


class LinkMapper(Cog):
    """Post one link, get another in a better place."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.guild is None:
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

        rows: list[LinkMapData] = response.json()

        for row in rows:
            if row.from_link in message.content:
                res = message.content.replace(row.from_link, row.to_link)

                await message.reply(res)

                break

    @group(aliases=("linkmap",))
    async def link_map(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @link_map.command()
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

    @link_map.command()
    @is_trusted()
    async def create_link_map(
        self,
        ctx: Context,
        from_match: str,
        to_match: str,
        xpath: str | None = None,
    ) -> None:
        data = {
            "channel_map_server_id": ctx.guild.id,
            "from_match": from_match,
            "to_match": to_match,
            "xpath": xpath,
        }

        response = await self.bot.api.post("/api/link_maps/converters", data=data)

        if not response.is_success:
            await ctx.send(f"Link map creation failed with code {response.status_code}")

            return

        await ctx.send("Link map created.")


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(LinkMapper(bot))


# from lxml import etree
# from bs4 import BeautifulSoup

# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
#             (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
#     "Accept-Language": "en-US, en;q=0.5",
# }
# REGEX_URL_MATCH = re.compile(r"https?://\S+")


# @dataclass
# class WebMapData:
#     id: int
#     server_id: int
#     user_id: int
#     created_at: datetime
#     matches: str
#     xpath: str


# class WebMapper(Cog):
#     """Retrieve an XPATH from a website."""

#     def __init__(self, bot: Xythrion):
#         self.bot = bot

#     @staticmethod
#     def get_first_url(message: str) -> str | None:
#         urls = re.findall(REGEX_URL_MATCH, message)

#         return urls[0] if len(urls) else None

#     @Cog.listener()
#     async def on_message(self, message: Message) -> None:
#         ...
#         # if message.guild is None:
#         #     return

#         # data = {"server_id": message.guild.id, "user_id": message.author.id}

#         # rows: list[WebMapData] = await self.bot.api.get("/api/web_maps/", params=data)

#         # for row in rows:
#         #     if row.matches in message.content:
#         #         full_url = self.get_first_url(message.content)
#         #         webpage = await self.bot.http_client.get(full_url, headers=HEADERS)
#         #         soup = BeautifulSoup(webpage.content, "html.parser")
#         #         dom = etree.HTML(str(soup))
#         #         extracted = dom.xpath(row.xpath)
#         #         xpath_url_extract = extracted[0].get("data-src")

#         #         await message.reply(xpath_url_extract)

#         #         break

#     @group(aliases=("webmap",))
#     @is_trusted()
#     async def web_map(self, ctx: Context) -> None:
#         if ctx.invoked_subcommand is None:
#             await ctx.send("Missing subcommand")

#     @web_map.command()
#     @is_trusted()
#     async def create_web_map(
#         self,
#         ctx: Context,
#         matches: str,
#         xpath: str,
#         guild_id: int | None = None,
#     ) -> None:
#         data = {
#             "user_id": ctx.author.id,
#             "created_at": ctx.message.created_at.replace(tzinfo=None),
#             "matches": matches,
#             "xpath": xpath,
#         }

#         if guild_id is not None:
#             data["server_id"] = guild_id
#         elif ctx.guild is not None:
#             data["server_id"] = ctx.guild.id
#         else:
#             await ctx.send(
#                 "Command sent was not in guild channel, and no guild channel specified.",
#             )

#             return

#         await self.bot.api.post("/api/web_maps/", data=data)

#     @web_map.command()
#     @is_trusted()
#     async def get_user_web_maps(
#         self,
#         ctx: Context,
#         guild_id: int | None = None,
#     ) -> None:
#         data = {"user_id": ctx.author.id}

#         j = await self.bot.api.get("/api/web_maps/", params=data)

#         await ctx.send(j)

#     @web_map.command()
#     @is_trusted()
#     async def remove_user_web_map(self, ctx: Context, id: int) -> None:
#         j = await self.bot.api.delete(f"/api/web_maps/{id}")

#         await ctx.send(j)


# async def setup(bot: Xythrion) -> None:
#     await bot.add_cog(WebMapper(bot))
