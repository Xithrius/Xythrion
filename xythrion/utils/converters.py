import re

from discord.ext.commands import Context, Converter

from xythrion.extensions import EXTENSIONS

whitespace_pattern = re.compile(r"\s+")
tuple_int_pattern = re.compile("^\((\d{1,3}), ?(\\d{1,3}), ?(\d{1,3})\)$")


def remove_whitespace(argument: str) -> str:
    """Replaces any whitespace within a string with nothingness."""
    return re.sub(whitespace_pattern, "", argument)


def convert_3d_tuples(argument: str) -> tuple[int, ...]:
    """From a string with 3 arguments to integers."""
    return tuple(int(x) for x in re.match(tuple_int_pattern, argument).groups())


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
