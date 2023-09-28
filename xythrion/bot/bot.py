import importlib
import inspect
import pkgutil
import sys
import traceback
from collections.abc import Iterator
from datetime import timedelta, timezone
from os import getenv
from typing import NoReturn

from discord import AllowedMentions, Embed, Intents, Interaction, Message, app_commands
from discord.ext.commands import Bot, CommandError
from dotenv import load_dotenv
from httpx import AsyncClient
from loguru import logger as log

from bot.api import APIClient
from bot.context import Context

from . import extensions

load_dotenv()


def walk_extensions() -> Iterator[str]:
    def on_error(name: str) -> NoReturn:
        raise ImportError(name=name)

    for module in pkgutil.walk_packages(
        extensions.__path__, f"{extensions.__name__}.", onerror=on_error
    ):
        if module.name.rsplit(".", maxsplit=1)[-1].startswith("_"):
            continue

        if module.ispkg:
            imported = importlib.import_module(module.name)
            if not inspect.isfunction(getattr(imported, "setup", None)):
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
        if isinstance(ctx, Interaction) or ctx.command is None:
            return

        log.error(f"Ignoring exception in command {ctx.command}:", file=sys.stderr)

        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )

        data = {"command_name": ctx.command.name, "successfully_completed": False}

        await self.api.post("/v1/command_metrics/", data=data)

        await ctx.send(embed=Embed(description=f"`{error}`"))

    async def on_command_completion(self, ctx: Context) -> None:
        if ctx.command is None:
            return

        data = {"command_name": ctx.command.name, "successfully_completed": True}

        await self.api.post("/v1/command_metrics/", data=data)

    async def setup_hook(self) -> None:
        """Things to setup before the bot logs on."""
        api_url = getenv("API_URL", "http://localhost:8000")

        self.api = APIClient(api_url)
        self.http_client = AsyncClient()

        for extension in EXTENSIONS:
            await self.load_extension(extension)

            ext_name = ".".join(extension.split(".")[-2:])
            log.info(f'Loading extension "{ext_name}"')

    async def start(self) -> None:
        """Things to run before bot starts."""
        token = getenv("BOT_TOKEN")

        if token is None:
            log.error("Retrieving token returned none")
            exit(1)

        await super().start(token=token)

    async def close(self) -> None:
        """Things to run before the bot logs off."""
        await self.api.aclose()
        await self.http_client.aclose()

        await super().close()

    @staticmethod
    async def on_ready() -> None:
        """Updates the bot status when logged in successfully."""
        log.info("Awaiting...")
