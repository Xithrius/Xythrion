import re

from discord import Embed
from discord.ext.commands import Cog, group

from bot.bot import Xythrion
from bot.context import Context

CVE_PATTERN = re.compile(r"CVE-\d{4}-\d{4,}")


# TODO: Pydantic models


class CVE(Cog):
    """CVE information."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @staticmethod
    def cve_embed_builder(
        title: str,
        description: str,
        url: str,
        published: str,
    ) -> Embed:
        embed = Embed(
            title=title,
            description=description,
            url=url,
        )
        embed.set_footer(text=f"Published on {published}")

        return embed

    @group()
    async def cve(self, ctx: Context) -> None:
        await ctx.check_subcommands()

    @cve.command()
    async def search(self, ctx: Context, cve: str) -> None:
        if CVE_PATTERN.match(cve) is not None:
            r = await self.bot.http_client.get(
                f"https://cveawg.mitre.org/api/cve/{cve}",
            )

            data = r.json()

            cve_url = f"https://www.cve.org/CVERecord?id={cve}"

            descriptions = data["containers"]["cna"]["descriptions"]
            published = data["cveMetadata"]["datePublished"]

            for desc in descriptions:
                if desc["lang"] == "en":
                    await ctx.send(
                        embed=self.cve_embed_builder(
                            cve,
                            desc["value"],
                            cve_url,
                            published,
                        ),
                    )

                    return

            await ctx.send(
                embed=self.cve_embed_builder(
                    cve,
                    "CVE found, but no English description was provided.",
                    cve_url,
                    published,
                ),
            )

            return

        await ctx.send(f"The input '{cve}' is not a valid CVE format.")


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(CVE(bot))
