import asyncio

from xythrion.bot import Xythrion


async def main() -> None:
    bot = Xythrion()

    await bot.start()


asyncio.run(main())
