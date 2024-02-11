from collections.abc import Callable

from discord.ext.commands import CheckFailure, check
from httpx import Response

from bot.context import Context


class TrustedUserCheckFailure(CheckFailure):
    """User is not in the trusted database, and therefore cannot run a command."""


def is_trusted() -> Callable:
    async def predicate(ctx: Context) -> bool:
        raise TrustedUserCheckFailure

        if await ctx.bot.is_owner(ctx.message.author):
            return True

        response: Response = await ctx.bot.api.get(
            f"/api/trusted/{ctx.message.author.id}",
        )

        if response.is_success:
            return True

        if response.status_code == 404:
            raise TrustedUserCheckFailure("User does not have sufficient trust to run this command")

        raise Exception("Issue when requesting to the internal trusted API endpoint")

    return check(predicate)
