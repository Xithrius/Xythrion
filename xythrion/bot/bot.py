import importlib
import inspect
import pkgutil
import sys
import traceback
from collections.abc import Iterator
from datetime import timedelta, timezone
from os import getenv
from typing import NoReturn

from bot.api import APIClient
from bot.context import Context
from discord import AllowedMentions, Embed, Intents, Interaction, Message, app_commands
from discord.ext.commands import Bot, CommandError
from dotenv import load_dotenv
from loguru import logger as log

from . import extensions

load_dotenv()


def unqualify(name: str) -> str:
    """Return an unqualified name given a qualified module/package `name`."""
    return name.rsplit(".", maxsplit=1)[-1]


def walk_extensions() -> Iterator[str]:
    """Yield extension names from the bot.extensions subpackage."""

    def on_error(name: str) -> NoReturn:
        raise ImportError(name=name)  # pragma: no cover

    for module in pkgutil.walk_packages(
        extensions.__path__, f"{extensions.__name__}.", onerror=on_error
    ):
        if unqualify(module.name).startswith("_"):
            # Ignore module/package names starting with an underscore.
            continue

        if module.ispkg:
            imported = importlib.import_module(module.name)
            if not inspect.isfunction(getattr(imported, "setup", None)):
                # If it lacks a setup function, it's not an extension.
                continue

        yield module.name


EXTENSIONS = frozenset(walk_extensions())


class Xythrion(Bot):
    """A subclass where important tasks and connections are created."""

    def __init__(self) -> None:
        """Initializing the bot with proper permissions."""
        intents = Intents.default()
        intents.members = True
        intents.message_content = True

        # https://stackoverflow.com/a/30712187
        timezone_offset: float = 0.0
        self.tzinfo = timezone(timedelta(hours=timezone_offset))

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
        api_url = getenv("API_URL", "http://localhost:8000")

        self.api = APIClient(api_url)

        for extension in EXTENSIONS:
            await self.load_extension(extension)
            log.info(f'Loadeding extension "{extension}"')

    async def start(self) -> None:
        """Things to run before bot starts."""
        token = getenv("BOT_TOKEN")

        if token is None:
            log.error("Retrieving token returned none")
            exit(1)

        await super().start(token=token)

    async def close(self) -> None:
        """Things to run before the bot logs off."""
        await self.api.close()

        await super().close()

    @staticmethod
    async def on_ready() -> None:
        """Updates the bot status when logged in successfully."""
        log.info("Awaiting...")
