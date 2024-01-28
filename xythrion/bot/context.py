from discord import Embed
from discord.ext.commands import Context as BaseContext
from discord.ext.commands import Group


class Context(BaseContext):
    """Definition of a custom context."""

    async def check_subcommands(self) -> None:
        if not isinstance(self.command, Group):
            raise AttributeError("command is not a group command")

        if self.invoked_subcommand is None:
            group: Group = self.command

            subcommands = ", ".join([f"`{cmd.name}`" for cmd in group.commands])

            embed = Embed(
                title="Missing subcommand",
                description=f"Possibilities: {subcommands}",
            )

            await self.send(embed=embed)
