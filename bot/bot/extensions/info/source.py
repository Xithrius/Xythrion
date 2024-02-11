import inspect
from pathlib import Path
from bot.context import Context

from discord import Embed
from discord.ext.commands import BadArgument, Cog, Command, HelpCommand, command

from bot.bot import Xythrion
from bot.constants import GITHUB_URL
from bot.utils.converters import SourceConverter, SourceType

DEPLOYMENT_FILE_PATH_PREFIX = Path("/project") / "pkgs"


def build_source_filepath(base_file_name: str) -> Path:
    stripped_path = Path(base_file_name).relative_to(DEPLOYMENT_FILE_PATH_PREFIX)
    return Path("xythrion", stripped_path)


class Source(Cog):
    """Displays information about the bot's source code."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    # TODO: Fix unhealthy state of this cog, since it does not work at the moment
    @command(aliases=("src",), enabled=False)
    async def source(
        self,
        ctx: Context,
        *,
        source_item: SourceConverter | None = None,
    ) -> None:
        """Display information and a GitHub link to the source code of a command, tag, or cog."""
        if not source_item:
            embed = Embed(title="Xythrion's GitHub Repository")
            embed.add_field(name="Repository", value=f"[Go to GitHub]({GITHUB_URL})")
            embed.set_thumbnail(url="https://avatars1.githubusercontent.com/u/9919")
            await ctx.send(embed=embed)
            return

        embed = await self.build_embed(source_item)
        await ctx.send(embed=embed)

    @staticmethod
    def get_source_link(source_item: SourceType) -> tuple[str, str, int | None]:
        """
        Build GitHub link of source item, return this link, file location and first line number.

        Raise BadArgument if `source_item` is a dynamically-created object (e.g. via internal eval).
        """
        if isinstance(source_item, Command):
            source_item = inspect.unwrap(source_item.callback)
            src = source_item.__code__
            filename = src.co_filename
        else:
            src = type(source_item)
            try:
                filename = inspect.getsourcefile(src)
            except TypeError:
                raise BadArgument("Cannot get source for a dynamically-created object.")

        try:
            lines, first_line_no = inspect.getsourcelines(src)
        except OSError:
            raise BadArgument("Cannot get source for a dynamically-created object.")

        lines_extension = f"#L{first_line_no}-L{first_line_no+len(lines)-1}"

        file_location = build_source_filepath(filename).as_posix()

        url = f"{GITHUB_URL}/blob/main/{file_location}{lines_extension}"

        return url, file_location, first_line_no or None

    async def build_embed(self, source_object: SourceType) -> Embed | None:
        """Build embed based on source object."""
        url, location, first_line = self.get_source_link(source_object)

        if isinstance(source_object, HelpCommand):
            title = "Help Command"
            description = (
                "[Discord's Default Help Command](https://discordpy.readthedocs.io"
                "/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand)"
            )
            return Embed(title=title, description=description)

        if isinstance(source_object, Command):
            description = source_object.short_doc
            title = f"Command: {source_object.qualified_name}"
        else:
            title = f"Cog: {source_object.qualified_name}"
            description = source_object.description.splitlines()[0]

        embed = Embed(title=title, description=description)
        embed.add_field(name="Source Code", value=f"[Go to GitHub]({url})")
        line_text = f":{first_line}" if first_line else ""
        embed.set_footer(text=f"{location}{line_text}")

        return embed


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Source(bot))
