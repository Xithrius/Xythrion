import time
from datetime import timedelta, timezone
from os import getenv

from discord import AllowedMentions, Intents, Message
from discord.ext.commands import Bot, when_mentioned_or
from dotenv import load_dotenv
from httpx import AsyncClient
from loguru import logger as log

from bot import extensions
from bot.api import APIClient
from bot.context import Context
from bot.utils import format_nanosecond_time, walk_extensions

load_dotenv()

API_HEALTHCHECK_ATTEMPTS = 5


class Xythrion(Bot):
    def __init__(self) -> None:
        """Initializing the bot with proper permissions."""
        intents = Intents.default()
        intents.members = True
        intents.message_content = True

        # https://stackoverflow.com/a/30712187
        timezone_offset: float = 0.0
        self.tzinfo = timezone(timedelta(hours=timezone_offset))

        self.command_prefix_str: str = getenv("BOT_PREFIX", "^")

        self.api: APIClient | None = None
        self.http_client: AsyncClient | None = None

        super().__init__(
            command_prefix=when_mentioned_or(self.command_prefix_str),
            case_insensitive=True,
            allowed_mentions=AllowedMentions(everyone=False),
            intents=intents,
        )

    async def get_context(self, message: Message, *, cls: Context = Context) -> Context:
        # noinspection PyTypeChecker
        return await super().get_context(message, cls=cls)

    async def on_command_completion(self, ctx: Context) -> None:
        if ctx.command is None:
            return

        data = {"command_name": ctx.command.name, "successfully_completed": True}

        await self.api.post("/api/command_metrics/", data=data)

    @staticmethod
    async def api_healthcheck(api: APIClient) -> bool:
        for i in range(API_HEALTHCHECK_ATTEMPTS):
            timeout = (i + 1) * 2
            log.info(f"({i + 1}/10): Attempting to connect to API, timeout of {timeout}...")
            response = await api.get("/api/health", timeout=timeout)

            if response.is_success:
                return True

        return False

    async def setup_hook(self) -> None:
        api_url = getenv("API_URL", "http://localhost:8001")

        log.info(f"Attempting to connect to API at {api_url}")
        self.api = APIClient(api_url)
        internal_api_health = await self.api_healthcheck(self.api)
        if not internal_api_health:
            log.critical("Attempted to connect to API, but failed. Exiting...")
            return

        self.http_client = AsyncClient()

        exts = list(walk_extensions(extensions))

        for extension in exts:
            start_time = time.perf_counter_ns()
            await self.load_extension(extension)
            end_time = time.perf_counter_ns()
            elapsed_ns = end_time - start_time
            elapsed_str = format_nanosecond_time(elapsed_ns)

            ext_name = ".".join(extension.split(".")[-2:])

            log.info(f"Loaded extension {ext_name} in {elapsed_str}")

    async def start(self, **kwargs) -> None:
        token = getenv("BOT_TOKEN")

        if token is None:
            log.error("Retrieving token returned none")
            exit(1)

        await super().start(token=token)

    async def close(self) -> None:
        await self.api.aclose()
        await self.http_client.aclose()

        await super().close()

    @staticmethod
    async def on_ready() -> None:
        log.info("Awaiting...")
