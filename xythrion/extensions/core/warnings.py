import sys
import traceback

from discord import Error
from discord.ext import commands
from discord.ext.commands import Cog
from loguru import logger as log

from xythrion.bot import Xythrion


class Warnings(Cog, command_attrs=dict(hidden=True)):
    """Warning a user about the actions that they've taken."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    async def on_command_error(self, ctx: commands.Context, error: Error) -> None:
        """Sending error information to the user."""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"'{error.param.name}' is a required argument.")
        else:
            log.error(
                f"Ignoring exception in command {ctx.command}:", file=sys.stderr
            )
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )
