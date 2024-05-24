import asyncio

import matplotlib

from .bot import Xythrion

matplotlib.use("agg")


async def main() -> None:
    bot = Xythrion()

    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
