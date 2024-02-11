from typing import TYPE_CHECKING

from discord import Embed
from discord.ext.commands import Context as BaseContext
from discord.ext.commands import Group

if TYPE_CHECKING:
    from bot.bot import Xythrion


class Context(BaseContext):
    """Definition of a custom context."""

    bot: "Xythrion"

    async def check_subcommands(self) -> None:
        if self.invoked_subcommand is not None:
            return

        if not isinstance(self.command, Group):
            raise AttributeError("command is not a group command")

        group: Group = self.command

        subcommands = "\n".join(
            [f"`{cmd.name} ({', '.join(cmd.aliases)})`" if cmd.aliases else f"`{cmd.name}`" for cmd in group.commands],
        )

        embed = Embed(
            title="Missing subcommand. Perhaps:",
            description=subcommands,
        )

        await self.send(embed=embed)
