import asyncio
import warnings
from collections.abc import Callable
from typing import Any

warnings.filterwarnings("ignore", category=UserWarning)


async def to_thread(func: Callable) -> Callable:
    async def decorator(*args, **kwargs) -> Any:
        return await asyncio.to_thread(func, *args, **kwargs)

    return decorator
