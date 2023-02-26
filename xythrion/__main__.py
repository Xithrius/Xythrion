import asyncio
import os

from dotenv import load_dotenv
from loguru import logger as log

from xythrion.bot import Xythrion


async def main():
    bot = Xythrion()
    await bot.start()


asyncio.run(main())
