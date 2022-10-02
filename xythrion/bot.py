from loguru import logger as log
from disnake.ext import commands


class Xythrion(commands.Bot):
    """A subclass where important tasks and connections are created."""

    def __init__(self, *args, **kwargs) -> None:
        """Creating import attributes."""
        super().__init__(*args, **kwargs)

    @staticmethod
    async def on_ready() -> None:
        """Updates the bot status when logged in successfully."""
        log.info("Awaiting...")
