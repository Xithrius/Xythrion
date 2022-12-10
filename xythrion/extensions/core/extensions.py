from discord.ext.commands import Cog, Context, ExtensionNotLoaded, group, is_owner
from loguru import logger as log

from xythrion.bot import Xythrion
from xythrion.extensions import EXTENSIONS
from xythrion.utils.converters import Extension
from xythrion.utils.formatting import codeblock


class Extensions(Cog):
    """Loading, unloading, reloading extensions."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @group(aliases=("extensions", "e"))
    @is_owner()
    async def extension(self, ctx: Context) -> None:
        """Extension group command."""
        if ctx.invoked_subcommand is None:
            await ctx.reply("Missing subcommand")

    @extension.command(aliases=("load",))
    async def load_extension(self, ctx: Context, extension: Extension) -> None:
        """Loads a singular extension."""
        await self.bot.load_extension(str(extension))

        await ctx.reply(f"Loaded extension {extension}.")

    @extension.command(aliases=("unload",))
    async def unload_extension(self, ctx: Context, extension: Extension) -> None:
        """Unloads a singular extension."""
        await self.bot.unload_extension(str(extension))

        await ctx.reply(f"Unloaded extension {extension}.")

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
                    f"Failed reloading {extension}.", exc_info=(type(e), e, e.__traceback__)
                )

        msg = f"Reloaded {len(EXTENSIONS)} extension(s)."

        log.info(msg)

        await ctx.send(msg)

    @extension.command(aliases=("list", "l", "cmds", "c"))
    async def list_commands(self, ctx: Context) -> None:
        """Lists all commands, and the extensions they're in."""
        cmd_list = sorted(
            [(k, v) for k, v in self.bot.cogs.items()],
            key=lambda x: x[0]
        )

        cmd_tree = []
        for (k, v) in cmd_list:
            if not v.get_commands():
                continue

            cmd_tree.append(k)

            for cmd in v.walk_commands():
                spacing = ' ' * (0 if cmd.parent is None else 3)
                cmd_tree.append(f'{spacing}└── {cmd.name}')

        await ctx.reply(codeblock(cmd_tree))
