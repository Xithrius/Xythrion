import re

from discord.ext.commands import Context, Converter

from bot import extensions
from bot.bot import walk_extensions

WHITESPACE_PATTERN = re.compile(r"\s+")
TUPLE_3D_INT_PATTERN = re.compile(r"^\((-?\d+),(-?\d+),(-?\d+)\)$")


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
