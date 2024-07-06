import time
from datetime import datetime, timedelta, timezone

from discord import AllowedMentions, Intents, Message
from discord.ext.commands import Bot, when_mentioned_or
from dotenv import load_dotenv
from httpx import AsyncClient as HttpxAsyncClient
from httpx import ConnectError
from loguru import logger as log

from bot import extensions
from bot.context import Context
from bot.settings import settings
from bot.utils import format_nanosecond_time, walk_extensions

load_dotenv()


class Xythrion(Bot):
    def __init__(self) -> None:
        intents = Intents.default()
        intents.members = True
        intents.message_content = True

        # https://stackoverflow.com/a/30712187
        timezone_offset: float = 0.0
        self.tzinfo = timezone(timedelta(hours=timezone_offset))
        self.startup_datetime: datetime | None = None

        self.internal_api: HttpxAsyncClient
        self.http_client: HttpxAsyncClient

        super().__init__(
            command_prefix=when_mentioned_or(settings.prefix),
            case_insensitive=True,
            allowed_mentions=AllowedMentions(everyone=False),
            intents=intents,
        )

    async def get_context(self, message: Message, *, cls: Context = Context) -> Context:  # type: ignore [assignment]
        return await super().get_context(message, cls=cls)

    @staticmethod
    async def __setup_internal_api_client() -> HttpxAsyncClient:
        base_url, internal_api_timeout = settings.internal_api_url, settings.internal_api_timeout

        log.info(f"Attempting to connect to internal API at {base_url}...")
        internal_api_client = HttpxAsyncClient(base_url=base_url, timeout=internal_api_timeout)

        try:
            await internal_api_client.get("/api/health")
        except ConnectError:
            log.critical("Attempted to connect to API, but failed. Exiting...")
            await internal_api_client.aclose()
            exit(1)

        log.info("Successfully created internal API client.")

        return internal_api_client

    async def setup_hook(self) -> None:
        self.internal_api_client = await self.__setup_internal_api_client()
        self.http_client = HttpxAsyncClient(timeout=settings.external_api_timeout)

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
        if (token := settings.token) is None:
            log.error("Discord token is not set at environment variable XYTHRION_BOT_TOKEN")
            exit(1)

        await super().start(token=token)

    async def close(self) -> None:
        await self.internal_api_client.aclose()
        await self.http_client.aclose()

        await super().close()

    async def on_ready(self) -> None:
        self.startup_datetime = datetime.now(self.tzinfo)

        log.info("Awaiting...")
