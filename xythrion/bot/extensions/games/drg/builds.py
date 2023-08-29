import json

from bot.context import Context
from discord.ext.commands import Cog, group

from bot.bot import Xythrion


class DeepRockGalacticBuilds(Cog):
    """Information about the game 'Deep Rock Galactic'."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group(aliases=("drgbuilds",))
    async def drg_builds(self, ctx: Context) -> None:
        """Group command for Deep Rock Galactic."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @drg_builds.command()
    async def get_builds(self, ctx: Context) -> None:
        data = await self.bot.api.get("/v1/drg/")

        await ctx.send(data)

    @drg_builds.command()
    async def create_build(
        self, ctx: Context, dwarf_class: str, build: str, overclock: str | None
    ) -> None:
        data = {
            "uid": ctx.author.id,
            "dwarf_class": dwarf_class,
            "build": build,
            "overclock": overclock,
        }

        await self.bot.api.post(
            "/v1/drg/",
            data=json.dumps(data, default=str),
        )


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(DeepRockGalacticBuilds(bot))
