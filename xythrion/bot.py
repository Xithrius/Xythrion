from discord import AllowedMentions, Intents
from discord.ext import commands
from loguru import logger as log


class Xythrion(commands.Bot):
    """A subclass where important tasks and connections are created."""

    def __init__(self) -> None:
        """Initializing the bot with proper permissions."""
        intents = Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix=commands.when_mentioned_or('.'),
            case_insensitive=True,
            help_command=None,
            allowed_mentions=AllowedMentions(everyone=False),
            intents=intents,
        )

    @staticmethod
    async def on_ready() -> None:
        """Updates the bot status when logged in successfully."""
        log.info("Awaiting...")
