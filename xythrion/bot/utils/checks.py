from collections.abc import Callable

from discord.ext.commands import check
from discord.ext.commands.errors import MissingPermissions
from httpx import Response

from bot.context import Context


def is_trusted() -> Callable:
    async def predicate(ctx: Context) -> bool:
        if await ctx.bot.is_owner(ctx.message.author):
            return True

        response: Response = await ctx.bot.api.get(
            f"/api/trusted/{ctx.message.author.id}",
        )

        if not response.is_success:
            raise MissingPermissions

        return True

    return check(predicate)
