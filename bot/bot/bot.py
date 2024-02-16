import time
from datetime import timedelta, timezone
from os import getenv

from discord import AllowedMentions, Intents, Message
from discord.ext.commands import Bot, when_mentioned_or
from dotenv import load_dotenv
from httpx import AsyncClient
from loguru import logger as log
from tabulate import tabulate

from bot import extensions
from bot.api import APIClient
from bot.constants import XYTHRION_LOGO
from bot.context import Context
from bot.utils import format_nanosecond_time, walk_extensions

load_dotenv()


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

        command_prefix: str = getenv("BOT_PREFIX", "^")

        super().__init__(
            command_prefix=when_mentioned_or(command_prefix),
            case_insensitive=True,
            allowed_mentions=AllowedMentions(everyone=False),
            intents=intents,
        )

    async def get_context(self, message: Message, *, cls: Context = Context) -> Context:
        """Defines the custom context."""
        return await super().get_context(message, cls=cls)

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
