import re

from discord.ext.commands import Converter

from bot.bot import EXTENSIONS
from bot.context import Context

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
    """
    Ensure the extension exists and return the full extension path.

    The `*` symbol represents all extensions.
    """

    async def convert(self, ctx: Context, argument: str) -> str:
        """Ensure the extension exists and return the full extension path."""
        argument = argument.lower()

        if "." not in argument:
            argument = f"xythrion.extensions.{argument}"

        if argument in EXTENSIONS:
            return argument

        raise ValueError(f"Invalid argument {argument}")
