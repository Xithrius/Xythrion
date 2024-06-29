from discord.ext.commands import Cog, ExtensionNotLoaded, group
from loguru import logger as log
from tabulate import tabulate  # type: ignore [import-untyped]

from bot import extensions
from bot.bot import Xythrion, walk_extensions
from bot.context import Context
from bot.utils import Extension, codeblock, is_trusted


class Extensions(Cog):
    """Loading, unloading, reloading extensions."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @group(aliases=("extensions", "e"))
    @is_trusted()
    async def extension(self, ctx: Context) -> None:
        """Extension group command."""
        await ctx.check_subcommands()

    @extension.command(aliases=("load",))
    @is_trusted()
    async def load_extension(self, ctx: Context, extension: Extension) -> None:
        """Loads a singular extension."""
        await self.bot.load_extension(str(extension))

        await ctx.send(f"Loaded extension {extension}.")

    @extension.command(aliases=("unload",))
    @is_trusted()
    async def unload_extension(self, ctx: Context, extension: Extension) -> None:
        """Unloads a singular extension."""
        await self.bot.unload_extension(str(extension))

        await ctx.send(f"Unloaded extension {extension}.")

    @extension.command(aliases=("reload", "r"))
    @is_trusted()
    async def reload_extensions(self, ctx: Context) -> None:
        """Reloads all extensions."""
        exts = list(walk_extensions(extensions))

        for extension in exts:
            try:
                await self.bot.reload_extension(extension)
            except ExtensionNotLoaded:
                await self.bot.load_extension(extension)
            except Exception as e:
                return log.error(
                    f"Failed reloading {extension}.",
                    exc_info=(type(e), e, e.__traceback__),
                )

        msg = f"Reloaded {len(exts)} extension(s)."

        log.info(msg)

        await ctx.send(msg)

        return None

    @extension.command(aliases=("list", "l"))
    async def list_extensions(self, ctx: Context, cog: str | None = None) -> None:
        """
        Lists all extensions and the amount of commands each one has.

        If a cog is specified, then all the commands that it contains are listed.
        """
        if (c := cog) is not None:
            try:
                cog_obj = self.bot.cogs[c]
                cmd_list = sorted([x.name for x in cog_obj.walk_commands()])
                block = tabulate({f"Name ({len(cmd_list)})": cmd_list}, headers="keys")

                await ctx.send(codeblock(block))
            except KeyError:
                await ctx.error_embed(f"Cog by the name of '{c}' could not be found")
            return

        ext_list = sorted(
            [(c[0], len(list(c[1].walk_commands()))) for c in self.bot.cogs.items()],
            key=lambda x: x[1],
            reverse=True,
        )

        block = tabulate(ext_list, headers=["Name", "Command count"])

        await ctx.send(codeblock(block))


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Extensions(bot))
