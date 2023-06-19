from discord.ext.commands import Cog, command, is_owner
from loguru import logger as log

from xythrion.bot import Xythrion
from xythrion.context import Context


class Administration(Cog):
    """Admin-specific commands."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command(alias=("logout",))
    @is_owner()
    async def shutdown(self, ctx: Context) -> None:
        """Shuts the bot down."""
        log.info("Logging out...")

        await self.bot.logout()
