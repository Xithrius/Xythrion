import os
import sys
import traceback

import asyncpg
import httpx
from discord import AllowedMentions, Embed, Intents, Interaction, Message, app_commands
from discord.ext.commands import (
    Bot,
    CommandError,
)
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


class Xythrion(Bot):
    """A subclass where important tasks and connections are created."""

    def __init__(self) -> None:
        """Initializing the bot with proper permissions."""
        intents = Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(
            command_prefix="^",
            case_insensitive=True,
            allowed_mentions=AllowedMentions(everyone=False),
            intents=intents,
        )

    async def get_context(self, message: Message, *, cls: Context = Context) -> Context:
        """Defines the custom context."""
        return await super().get_context(message, cls=cls)

    async def on_command_error(
        self,
        ctx: Context | Interaction,
        error: CommandError | app_commands.AppCommandError,
    ) -> None:
        """Reporting errors to the console and the user."""
        log.error(f"Ignoring exception in command {ctx.command}:", file=sys.stderr)

        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )

        await ctx.send(embed=Embed(description=f"`{error}`"))

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
        await self.http_client.aclose()

        await self.pool.close()

        await super().close()

    @staticmethod
    async def on_ready() -> None:
        """Updates the bot status when logged in successfully."""
        log.info("Awaiting...")
