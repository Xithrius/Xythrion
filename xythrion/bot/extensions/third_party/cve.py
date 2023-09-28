import re

from discord import Embed
from discord.ext.commands import Cog, group

from bot.bot import Xythrion
from bot.context import Context

CVE_PATTERN = re.compile(r"CVE-\d{4}-\d{4,}")


class CVE(Cog):
    """CVE information."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @group()
    async def cve(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @cve.command()
    async def search(self, ctx: Context, cve: str) -> None:
        if CVE_PATTERN.match(cve) is not None:
            r = await self.bot.http_client.get(
                f"https://cveawg.mitre.org/api/cve/{cve}"
            )

            data = r.json()

            cve_url = f"[{cve}](https://www.cve.org/CVERecord?id={cve})"

            descriptions = data["containers"]["cna"]["descriptions"]

            for desc in descriptions:
                if desc["lang"] == "en":
                    embed = Embed(title=desc["value"], description=cve_url)

                    await ctx.send(embed=embed)

                    return

            embed = Embed(
                title="CVE found, but no English description was provided.",
                description=cve_url,
            )

            await ctx.send(embed=embed)

            return

        await ctx.send(f"The input '{cve}' is not a valid CVE format.")


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(CVE(bot))
