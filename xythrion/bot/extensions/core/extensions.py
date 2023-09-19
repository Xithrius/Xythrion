from discord.ext.commands import Cog, ExtensionNotLoaded, group
from loguru import logger as log

from bot.bot import EXTENSIONS, Xythrion
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
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @extension.command(aliases=("load",))
    async def load_extension(self, ctx: Context, extension: Extension) -> None:
        """Loads a singular extension."""
        await self.bot.load_extension(str(extension))

        await ctx.send(f"Loaded extension {extension}.")

    @extension.command(aliases=("unload",))
    async def unload_extension(self, ctx: Context, extension: Extension) -> None:
        """Unloads a singular extension."""
        await self.bot.unload_extension(str(extension))

        await ctx.send(f"Unloaded extension {extension}.")

    @extension.command(aliases=("reload", "r"))
    async def reload_extensions(self, ctx: Context) -> None:
        """Reloads all extensions."""
        for extension in EXTENSIONS:
            try:
                await self.bot.reload_extension(extension)
            except ExtensionNotLoaded:
                await self.bot.load_extension(extension)
            except Exception as e:
                return log.error(
                    f"Failed reloading {extension}.",
                    exc_info=(type(e), e, e.__traceback__),
                )

        msg = f"Reloaded {len(EXTENSIONS)} extension(s)."

        log.info(msg)

        await ctx.send(msg)
        return None

    @extension.command(aliases=("list", "l", "cmds", "c"))
    async def list_commands(self, ctx: Context) -> None:
        """Lists all commands, and the extensions they're in."""
        cmd_list = sorted(self.bot.cogs.items(), key=lambda x: x[0])

        cmd_tree = []
        for k, v in cmd_list:
            if not v.get_commands():
                continue

            cmd_tree.append(k)

            cmds = list(v.walk_commands())

            for i, cmd in enumerate(cmds):
                spacing: str
                if cmd.parent is None:
                    spacing = ""
                else:
                    spacing = "│" + " " * 3

                tree: str
                if i == (len(cmds) - 1):
                    tree = "└──"
                else:
                    tree = "├──"

                cmd_tree.append(f"{spacing}{tree} {cmd.name}")

        await ctx.send(codeblock(cmd_tree))


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Extensions(bot))
