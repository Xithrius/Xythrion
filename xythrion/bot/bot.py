import importlib
import inspect
import pkgutil
import sys
import time
import traceback
import types
from collections.abc import Iterator
from datetime import timedelta, timezone
from os import getenv
from typing import NoReturn

from discord import AllowedMentions, Embed, Intents, Interaction, Message, app_commands
from discord.ext.commands import Bot, CommandError, when_mentioned_or
from dotenv import load_dotenv
from httpx import AsyncClient
from loguru import logger as log
from tabulate import tabulate

from bot import extensions
from bot.api import APIClient
from bot.constants import XYTHRION_LOGO
from bot.context import Context
from bot.extensions.core._utils.formatting import format_nanosecond_time

load_dotenv()


def ignore_module(module: pkgutil.ModuleInfo) -> bool:
    return any(name.startswith("_") for name in module.name.split("."))


def walk_extensions(module: types.ModuleType) -> Iterator[str]:
    def on_error(name: str) -> NoReturn:
        raise ImportError(name=name)

    modules = set()

    for module_info in pkgutil.walk_packages(module.__path__, f"{module.__name__}.", onerror=on_error):
        if ignore_module(module_info):
            continue

        if module_info.ispkg:
            imported = importlib.import_module(module_info.name)
            if not inspect.isfunction(getattr(imported, "setup", None)):
                continue

        modules.add(module_info.name)

    return frozenset(modules)


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
            command_prefix=when_mentioned_or("^"),
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
            type(error),
            error,
            error.__traceback__,
            file=sys.stderr,
        )

        data = {"command_name": ctx.command.name, "successfully_completed": False}

        await self.api.post("/api/command_metrics/", data=data)

        await ctx.send(embed=Embed(description=f"`{error}`"))

    async def on_command_completion(self, ctx: Context) -> None:
        if ctx.command is None:
            return

        data = {"command_name": ctx.command.name, "successfully_completed": True}

        await self.api.post("/api/command_metrics/", data=data)

    async def setup_hook(self) -> None:
        """Things to setup before the bot logs on."""
        api_url = getenv("API_URL", "http://localhost:8001")

        self.api = APIClient(api_url)
        self.http_client = AsyncClient()

        print(XYTHRION_LOGO)  # noqa: T201

        exts = list(walk_extensions(extensions))

        ext_times = []

        for extension in exts:
            start_time = time.perf_counter_ns()
            await self.load_extension(extension)
            end_time = time.perf_counter_ns()
            elapsed_ns = end_time - start_time
            elapsed_str = format_nanosecond_time(elapsed_ns)

            ext_name = ".".join(extension.split(".")[-2:])
            ext_times.append((ext_name, elapsed_ns, elapsed_str))

        print(  # noqa: T201
            tabulate(
                [[x[0], x[2]] for x in sorted(ext_times, key=lambda x: x[1])],
                headers=["Cog", "Load time"],
                colalign=["right", "left"],
            ),
            end="\n\n",
        )

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
