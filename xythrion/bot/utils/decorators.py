import asyncio
from collections.abc import Callable, Coroutine
from typing import Any


def to_async(func: Callable) -> Coroutine[Any, Any, Any]:
    async def wrapper(*args, **kwargs) -> Any:
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper
