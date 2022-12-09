import asyncio
import os

from dotenv import load_dotenv
from loguru import logger as log

from xythrion.bot import Xythrion
from xythrion.extensions import EXTENSIONS


async def load_extensions() -> None:
    """Loads extensions in an async type of way."""
    for extension in EXTENSIONS:
        await bot.load_extension(extension)
        log.info(f'Loaded extension "{extension}"')


load_dotenv()

bot = Xythrion()

asyncio.run(load_extensions())

token = os.getenv("BOT_TOKEN")
if token is None:
    log.error("Retrieving token returned none")
    exit(1)

bot.run(token=token)
