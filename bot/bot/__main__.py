import asyncio

from .bot import Xythrion


async def main() -> None:
    bot = Xythrion()

    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
