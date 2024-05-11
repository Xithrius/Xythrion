import sys
import traceback

from discord.ext.commands import Cog, errors
from loguru import logger as log

from bot.bot import Xythrion
from bot.context import Context
from bot.utils.checks import TrustedUserCheckFailure


class CommandErrorHandler(Cog):
    """Handling command errors."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, e: errors.CommandError) -> None:
        if isinstance(e, errors.CommandNotFound):
            await ctx.error_embed("That command does not exist")
            return
        if isinstance(e, TrustedUserCheckFailure):
            await ctx.error_embed(
                "You do not have sufficient trust to run this command",
            )
            return

        log.error("Ignoring exception in command")
        traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)

        await ctx.error_embed(str(e))


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(CommandErrorHandler(bot))
