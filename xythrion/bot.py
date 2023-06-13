import os

import asyncpg
import httpx
from discord import AllowedMentions, Intents, Message
from discord.ext import commands
from dotenv import load_dotenv
from loguru import logger as log

from xythrion.context import Context
from xythrion.extensions import EXTENSIONS

load_dotenv()


POSTGRES_CREDENTIALS = {
    "user": "xythrion",
    "password": "xythrion",
    "database": "xythrion",
    "port": 7777,
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

    async def get_context(self, message: Message, *, cls: Context = Context) -> Context:
        """Defines the custom context."""
        return await super().get_context(message, cls=cls)

    async def setup_hook(self) -> None:
        """Things to setup before the bot logs on."""
        self.http_client = httpx.AsyncClient()

        self.pool = await asyncpg.create_pool(
            **POSTGRES_CREDENTIALS, command_timeout=60
        )

        for extension in EXTENSIONS:
            await self.load_extension(extension)
            log.info(f'Loaded extension "{extension}"')

    async def start(self) -> None:
        """Things to run before bot starts."""
        token = os.getenv("BOT_TOKEN")

        if token is None:
            log.error("Retrieving token returned none")
            exit(1)

        await super().start(token=token)

    async def close(self) -> None:
        """Things to run before the bot logs off."""
        await self.http_client.close()

        self.pool.close()

        await super().close()

    @staticmethod
    async def on_ready() -> None:
        """Updates the bot status when logged in successfully."""
        log.info("Awaiting...")
