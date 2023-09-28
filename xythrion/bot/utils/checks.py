from collections.abc import Callable

from discord.ext.commands import check
from httpx import Response

from bot.context import Context


def is_trusted() -> Callable:
    async def predicate(ctx: Context) -> bool:
        if await ctx.bot.is_owner(ctx.message.author):
            return True

        response: Response = await ctx.bot.api.get(
            f"/v1/trusted/{ctx.message.author.id}"
        )

        return response.is_success

    return check(predicate)
