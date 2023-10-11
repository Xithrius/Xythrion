from discord.ext.commands import Cog, group

from bot.bot import Xythrion
from bot.context import Context


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
        data = await self.bot.api.get("/api/drg/")

        await ctx.send(data)

    @drg_builds.command()
    async def create_build(
        self,
        ctx: Context,
        dwarf_class: str,
        build: str,
        overclock: str | None,
    ) -> None:
        data = {
            "user_id": ctx.author.id,
            "dwarf_class": dwarf_class,
            "build": build,
            "overclock": overclock,
        }

        await self.bot.api.post("/api/drg/", data=data)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(DeepRockGalacticBuilds(bot))
