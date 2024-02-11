import sys
import traceback
from random import choice

from discord import Colour, Embed
from discord.ext.commands import Cog
from discord.ext.commands.errors import CommandError
from loguru import logger as log

from bot.bot import Xythrion
from bot.constants import ERROR_REPLIES
from bot.context import Context
from bot.utils.checks import TrustedUserCheckFailure


class CommandErrorHandler(Cog):
    """Handling command errors."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @staticmethod
    def error_embed(message: str) -> Embed:
        return Embed(
            title=choice(ERROR_REPLIES),
            description=message,
            colour=Colour.red(),
        )

    @Cog.listener()
    async def on_command_error(self, ctx: Context, e: CommandError) -> None:
        if ctx.command is not None:
            await ctx.bot.api.post(
                "/api/command_metrics/",
                data={"command_name": ctx.command.name, "successfully_completed": False},
            )

        if isinstance(e, TrustedUserCheckFailure):
            await ctx.send(embed=self.error_embed("You do not have sufficient trust to run this command"))

            return

        log.error("Ignoring exception in command")
        traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)

        await ctx.send(embed=self.error_embed(str(e)))


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(CommandErrorHandler(bot))
