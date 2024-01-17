from collections.abc import Callable

from discord.ext.commands import check
from discord.ext.commands.errors import MissingPermissions
from httpx import Response

from bot.bot import Xythrion
from bot.context import Context


def is_trusted() -> Callable:
    async def predicate(ctx: Context) -> bool:
        if await ctx.bot.is_owner(ctx.message.author):
            return True

        bot: Xythrion = ctx.bot

        response: Response = await bot.api.get(
            f"/api/trusted/{ctx.message.author.id}",
        )

        if not response.is_success:
            raise MissingPermissions

        return True

    return check(predicate)
