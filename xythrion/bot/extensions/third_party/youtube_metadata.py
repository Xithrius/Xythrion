from discord.ext.commands import Cog, group

from bot.bot import Xythrion
from bot.context import Context


class YoutubeMetadata(Cog):
    """Metadata for YouTube videos."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @group(aliases=("yt",))
    async def youtube(self, ctx: Context) -> None:
        await ctx.check_subcommands()

    @youtube.command()
    async def thumbnail(self, ctx: Context, id: str, quality: int | None = 0) -> None:
        if quality not in range(4):
            await ctx.send("Quality must be anywhere from 0 to 3.")

        url = f"https://img.youtube.com/vi/{id}/{quality}.jpg"

        await ctx.send(url)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(YoutubeMetadata(bot))
