from io import BytesIO
from uuid import uuid4

from discord import Embed, File
from discord.ext.commands import Context as BaseContext


class Context(BaseContext):
    """Definition of a custom context."""

    async def send_buffer(self, buffer: BytesIO, embed: Embed = None) -> None:
        """Send the contents of a buffer as an image to a context."""
        if embed is None:
            embed = Embed()

        file_name = uuid4()

        embed.set_image(url=f"attachment://{file_name}.png")

        file = File(fp=buffer, filename=f"{file_name}.png")

        await self.send(embed=embed, file=file)
