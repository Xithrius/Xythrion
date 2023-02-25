import asyncio
import functools
from typing import Any, Callable


def noblock(func: Callable) -> Any:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        sync_func = functools.partial(func, *args, **kwargs)

        return await asyncio.get_event_loop().run_in_executor(None, sync_func)

    return wrapper
