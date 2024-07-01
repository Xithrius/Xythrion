import asyncio
import inspect
from asyncio import Task
from pathlib import Path

from discord.ext.commands import Cog, ExtensionNotLoaded, group
from loguru import logger as log
from pydantic import BaseModel
from tabulate import tabulate  # type: ignore [import-untyped]

from bot import extensions
from bot.bot import Xythrion, walk_extensions
from bot.context import Context
from bot.settings import settings
from bot.utils import Extension, codeblock, is_trusted


class ExtensionInfo(BaseModel):
    abs_path: Path
    mtime_ns: int


class Extensions(Cog):
    """Loading, unloading, reloading extensions."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

        self.extension_autoreload_bg_task: Task[None] | None
        self.extension_mtimes_ns: dict[str, ExtensionInfo] | None

        if settings.environment == "dev":
            log.info("Development environment enabled, cogs will be auto-reloaded upon modification")
            self.extension_autoreload_bg_task = self.bot.loop.create_task(self.autoreload_extensions())
        else:
            log.warning("This is not a development environment, so extension auto-reloading is disabled")

    async def cog_unload(self) -> None:
        if self.extension_autoreload_bg_task is not None:
            log.info("Stopping extensions autoreload...")

            self.extension_autoreload_bg_task.cancel()

    def set_extension_mtimes_ns(self) -> None:
        log.info("Setting initial extension file modification times")

        self.extension_mtimes_ns = {}

        for _, ext in self.bot.extensions.items():
            path_from_module = inspect.getfile(ext)
            file = Path(path_from_module)

            if file.exists() and file.is_file():
                last_modified_ns = file.stat().st_mtime_ns

                self.extension_mtimes_ns[ext.__name__] = ExtensionInfo(
                    abs_path=file,
                    mtime_ns=last_modified_ns,
                )

    async def check_and_reload_extensions(self) -> None:
        if (ext_mtimes_ns := self.extension_mtimes_ns) is not None:
            for ext_module_path, ext_info in ext_mtimes_ns.items():
                current_mtime_ns = ext_info.abs_path.stat().st_mtime_ns

                # File was modified
                if current_mtime_ns > ext_info.mtime_ns:
                    log.info(f"Reloaded {ext_module_path}")
                    await self.bot.reload_extension(ext_module_path)
                    ext_mtimes_ns[ext_module_path].mtime_ns = current_mtime_ns

    async def autoreload_extensions(self) -> None:
        await self.bot.wait_until_ready()

        interval = settings.extensions_autoreload_check_interval

        log.info(f"Auto-reload extensions task loaded, listening for extension changes every {interval}s...")

        self.set_extension_mtimes_ns()

        while not self.bot.is_closed():
            await self.check_and_reload_extensions()

            await asyncio.sleep(interval)

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
