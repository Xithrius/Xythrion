import sys
import traceback

from discord.ext import commands
from discord.ext.commands import Cog
from loguru import logger as log

from xythrion.bot import Xythrion
from xythrion.context import Context


class Warnings(Cog, command_attrs=dict(hidden=True)):
    """Warning a user about the actions that they've taken."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @staticmethod
    async def on_command_error(
        ctx: Context, error: commands.CommandError
    ) -> None:
        """Handling all sorts of errors."""
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(
                "I could not find member '{error.argument}'. Please try again"
            )

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"'{error.param.name}' is a required argument.")
        else:
            # All unhandled errors will print their original traceback
            log.error(
                f"Ignoring exception in command {ctx.command}:", file=sys.stderr
            )
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )
