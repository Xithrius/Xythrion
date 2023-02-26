from discord import AllowedMentions, Intents
from discord.ext import commands
from loguru import logger as log
import asyncpg
import asyncio
import functools
from xythrion.extensions import EXTENSIONS
import os

from dotenv import load_dotenv

load_dotenv()


POSTGRES_CREDENTIALS = {
    "user": "xythrion",
    "password": "xythrion",
    "database": "xythrion",
    "port": 7777
}


class Xythrion(commands.Bot):
    """A subclass where important tasks and connections are created."""

    def __init__(self) -> None:
        """Initializing the bot with proper permissions."""
        intents = Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(
            command_prefix="\\",
            case_insensitive=True,
            help_command=None,
            allowed_mentions=AllowedMentions(everyone=False),
            intents=intents,
        )

    async def setup_hook(self):
        # self.session = aiohttp.ClientSession()

        self.pool = await asyncpg.create_pool(
            **POSTGRES_CREDENTIALS, command_timeout=60
        )

        for extension in EXTENSIONS:
            await self.load_extension(extension)
            log.info(f'Loaded extension "{extension}"')

    async def start(self):
        token = os.getenv("BOT_TOKEN")

        if token is None:
            log.error("Retrieving token returned none")
            exit(1)

        await super().start(token=token)

    async def close(self):
        # await self.session.close()

        self.pool.close()

        return await super().close()

    @staticmethod
    async def on_ready() -> None:
        """Updates the bot status when logged in successfully."""
        log.info("Awaiting...")
