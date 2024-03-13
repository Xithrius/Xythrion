from io import BytesIO
from random import choice
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from discord import Embed, File
from discord.ext.commands import Context as BaseContext
from discord.ext.commands import Group

from bot.constants import ERROR_REPLIES, POSITIVE_REPLIES, WARNING_REPLIES, Colours

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

        await self.warning_embed(
            subcommands,
            title="Missing subcommand. Perhaps one of these?",
        )

    async def send_image_buffer(
        self,
        buffer: BytesIO,
        *,
        embed: Embed | None = None,
        file_name: str | UUID | None = None,
    ) -> None:
        embed = embed or Embed()
        file_name = file_name or uuid4()

        embed.set_image(url=f"attachment://{file_name}.png")

        file = File(fp=buffer, filename=f"{file_name}.png")

        await self.send(embed=embed, file=file)

    @staticmethod
    def __construct_reply_embed(
        description: str,
        title: str | None,
        color: Colours,
        replies: tuple[str],
    ) -> Embed:
        embed = Embed(
            title=title or choice(replies),
            description=description,
            colour=color,
        )

        return embed

    async def error_embed(self, description: str, title: str | None = None) -> Embed:
        await self.send(
            embed=self.__construct_reply_embed(
                description,
                title,
                Colours.soft_red,
                ERROR_REPLIES,
            ),
        )

    async def warning_embed(self, description: str, title: str | None = None) -> Embed:
        await self.send(
            embed=self.__construct_reply_embed(
                description,
                title,
                Colours.soft_orange,
                WARNING_REPLIES,
            ),
        )

    async def success_embed(self, description: str, title: str | None = None) -> Embed:
        await self.send(
            embed=self.__construct_reply_embed(
                description,
                title,
                Colours.soft_green,
                POSITIVE_REPLIES,
            ),
        )
