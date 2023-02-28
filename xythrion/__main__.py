import asyncio

from xythrion.bot import Xythrion


async def main():
    bot = Xythrion()
    await bot.start()


asyncio.run(main())
