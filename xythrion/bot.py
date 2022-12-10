from discord import AllowedMentions, Intents
from discord.ext import commands
from loguru import logger as log


class Xythrion(commands.Bot):
    """A subclass where important tasks and connections are created."""

    def __init__(self) -> None:
        """Creating import attributes."""
        super().__init__(
            command_prefix=commands.when_mentioned,
            case_insensitive=True,
            help_command=None,
            allowed_mentions=AllowedMentions(everyone=False),
            intents=Intents.default(),
        )

    @staticmethod
    async def on_ready() -> None:
        """Updates the bot status when logged in successfully."""
        log.info("Awaiting...")
