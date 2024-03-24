import asyncio
from typing import Any
from collections.abc import Callable, Coroutine


def to_async(func: Callable) -> Callable[..., Coroutine[Any, Any, Any]]:
    async def wrapper(*args, **kwargs) -> Any:
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper
