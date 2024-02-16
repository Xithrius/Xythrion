import re
from typing import TYPE_CHECKING

from discord.ext.commands import Cog, Command, Converter, ExtensionNotLoaded, HelpCommand

from bot import extensions
from bot.context import Context

if TYPE_CHECKING:
    from bot.bot import walk_extensions


WHITESPACE_PATTERN = re.compile(r"\s+")
TUPLE_3D_INT_PATTERN = re.compile(r"^\((-?\d+),(-?\d+),(-?\d+)\)$")

SourceType = HelpCommand | Command | Cog | ExtensionNotLoaded


def remove_whitespace(argument: str) -> str:
    """Replaces any whitespace within a string with nothingness."""
    return re.sub(WHITESPACE_PATTERN, "", argument)


def convert_3d_tuples(argument: str) -> tuple[int, int, int]:
    """From a string with 3 arguments to integers."""
    int3 = tuple(int(x) for x in re.match(TUPLE_3D_INT_PATTERN, argument).groups())

    if len(int3) != 3:
        raise ValueError("Argument could not be converted to tuple of 3 integers")

    return int3


class Extension(Converter):
    async def convert(self, ctx: Context, argument: str) -> str:
        argument = argument.lower()

        if "." not in argument:
            argument = f"bot.extensions.{argument}"

        exts = walk_extensions(extensions)

        if argument in exts:
            return argument

        raise ValueError(f"Invalid argument {argument}")


class SourceConverter(Converter):
    """Convert an argument into a help command, command, or cog."""

    @staticmethod
    async def convert(ctx: Context, argument: str) -> SourceType | None:
        """Convert argument into source object."""
        if argument.lower() == "help":
            return ctx.bot.help_command

        return ctx.bot.get_cog(argument) or ctx.bot.get_command(argument)
