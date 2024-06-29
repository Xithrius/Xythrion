from discord import Embed
from discord.ext.commands import Cog, group
from httpx import AsyncClient
from loguru import logger as log
from pydantic import BaseModel

from bot.bot import Xythrion
from bot.context import Context

MODRINTH_SITE_BASE_URL = "https://modrinth.com"
MODRINTH_BASE_API_ENDPOINT = "https://api.modrinth.com/v2"
MODRINTH_ICON_URL = "https://avatars.githubusercontent.com/u/67560307?s=280&v=4"


class Hit(BaseModel):
    project_id: str
    project_type: str
    slug: str
    author: str
    title: str
    description: str
    categories: list[str]
    display_categories: list[str]
    versions: list[str]
    downloads: int
    follows: int
    icon_url: str
    date_created: str
    date_modified: str
    latest_version: str
    license: str
    client_side: str
    server_side: str
    gallery: list[str]
    featured_gallery: str | None
    color: int


class ProjectSearchResults(BaseModel):
    hits: list[Hit]
    offset: int
    limit: int
    total_hits: int


class Modrinth(Cog):
    """Mods from the Modrinth API."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

        self.modrinth_api: AsyncClient

    async def cog_load(self) -> None:
        log.info("Creating API client for Modrinth...")

        self.modrinth_api = AsyncClient(base_url=MODRINTH_BASE_API_ENDPOINT)

    @group()
    async def modrinth(self, ctx: Context) -> None:
        await ctx.check_subcommands()

    @modrinth.command(name="search", aliases=("query",))
    async def modrinth_project_search(self, ctx: Context, *, query: str) -> None:
        def __build_results_embed(results: ProjectSearchResults) -> Embed:
            e = Embed(title=f"Search results for *{query}*")
            e.set_author(name="Modrinth", icon_url=MODRINTH_ICON_URL)

            descriptions = []
            for hit in results.hits[:5]:
                url = f"{MODRINTH_SITE_BASE_URL}/{hit.project_type}/{hit.slug}"
                descriptions.append([f"**[{hit.title}]({url})**", hit.description.replace("\n", " ")])

            e.description = "\n\n".join("\n".join(x) for x in descriptions)

            return e

        params = {"query": query}
        response = await self.modrinth_api.get(
            "/search",
            params=params,
        )

        data = ProjectSearchResults(**response.json())

        embed = __build_results_embed(data)

        await ctx.send(embed=embed)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Modrinth(bot))
