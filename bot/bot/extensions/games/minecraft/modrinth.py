from discord import Embed
from discord.ext.commands import Cog, group
from httpx import AsyncClient
from loguru import logger as log

from bot.bot import Xythrion
from bot.context import Context

from ._models.modrinth.project import ProjectResult
from ._models.modrinth.search import ProjectSearchResults

MODRINTH_SITE_BASE_URL = "https://modrinth.com"
MODRINTH_BASE_API_ENDPOINT = "https://api.modrinth.com/v2"
MODRINTH_ICON_URL = "https://avatars.githubusercontent.com/u/67560307?s=280&v=4"


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

    @modrinth.command(name="search", aliases=("s", "query", "q"))
    async def modrinth_project_search(self, ctx: Context, *, query: str) -> None:
        def __build_results_embed(results: ProjectSearchResults) -> Embed:
            e = Embed(title=f"Search results for *{query}*")
            e.set_author(name="Modrinth", icon_url=MODRINTH_ICON_URL, url=MODRINTH_SITE_BASE_URL)

            descriptions = []
            for hit in results.hits[:5]:
                url = f"{MODRINTH_SITE_BASE_URL}/{hit.project_type}/{hit.slug}"
                title = f"**[{hit.title}]({url})** ({hit.author}) - **{hit.project_type}**"
                description = hit.description.replace("\n", " ")

                descriptions.append([title, description])

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

    @modrinth.command(name="project", aliases=("p",))
    async def modrinth_single_project_fetch(self, ctx: Context, *, project: str) -> None:
        def __build_project_result_embed(result: ProjectResult) -> Embed:
            url = f"{MODRINTH_SITE_BASE_URL}/{result.project_type}/{result.slug}"

            e = Embed(url=MODRINTH_SITE_BASE_URL)
            e.set_author(name="Modrinth", icon_url=MODRINTH_ICON_URL)
            e.set_thumbnail(url=result.icon_url)

            header = [
                f"**[{result.title}]({url})** - **{result.project_type}**",
                result.description.replace("\n", " "),
            ]

            supported_game_versions = (
                f"{result.game_versions[0]}"
                if len(result.game_versions) == 0
                else f"**>=** {result.game_versions[0]}, **<=** {result.game_versions[-1]}"
            )
            versions = ["**Versions**", supported_game_versions]

            support = [
                "**Support**",
                f"Client side: {result.client_side}",
                f"server side: {result.server_side}",
            ]

            descriptions = [header, versions, support]

            e.description = "\n\n".join("\n".join(x) for x in descriptions)

            return e

        response = await self.modrinth_api.get(f"/project/{project}")

        if response.status_code == 404:
            await ctx.error_embed(f"Modrinth project by the name of '{project}' could not be found.")
            return

        data = ProjectResult(**response.json())

        embed = __build_project_result_embed(data)

        await ctx.send(embed=embed)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Modrinth(bot))
