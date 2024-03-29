import re
from typing import TYPE_CHECKING

from discord.ext.commands import (
    Cog,
    Command,
    Converter,
    ExtensionNotLoaded,
    HelpCommand,
)

from bot import extensions
from bot.context import Context

if TYPE_CHECKING:
    from bot.bot import walk_extensions

WHITESPACE_PATTERN = re.compile(r"\s+")
TUPLE_3D_INT_PATTERN = re.compile(r"^\((-?\d+),(-?\d+),(-?\d+)\)$")

SourceType = HelpCommand | Command | Cog | ExtensionNotLoaded


def remove_whitespace(s: str) -> str:
    s = s.lower()

    return re.sub(WHITESPACE_PATTERN, "", s)


def str_to_tuple3(s: str) -> tuple[int, int, int]:
    s = s.lower()

    if (m := re.match(TUPLE_3D_INT_PATTERN, s)) is None:
        raise ValueError("No groups found in match")

    groups = m.groups()

    int3 = tuple(int(x) for x in groups)

    if len(int3) != 3:
        raise ValueError("Argument could not be converted to tuple of 3 integers")

    return int3


class Extension(Converter):
    @staticmethod
    async def convert(ctx: Context, argument: str) -> str:
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
    async def convert(ctx: Context, argument: str, **kwargs) -> SourceType | None:  # type: ignore [valid-type]
        """Convert argument into source object."""
        if argument.lower() == "help":
            return ctx.bot.help_command

        return ctx.bot.get_cog(argument) or ctx.bot.get_command(argument)
