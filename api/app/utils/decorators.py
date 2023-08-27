import asyncio
import functools
from typing import Any
from collections.abc import Callable


async def noblock(func: Callable) -> Any:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        sync_func = functools.partial(func, *args, **kwargs)

        return await asyncio.to_thread(sync_func)

    return wrapper