from io import BytesIO

from discord import Embed
from discord.ext.commands import Context as BaseContext

from bot.utils import send_image_buffer


class Context(BaseContext):
    """Definition of a custom context."""

    async def send_buffer(self, buffer: BytesIO, embed: Embed | None = None) -> None:
        """Send the contents of a buffer as an image to a context."""
        await send_image_buffer(buffer, ctx=self, embed=embed)
