from uuid import uuid4

from discord import Embed, File
from discord.ext.commands import Context as BaseContext


class Context(BaseContext):
    async def send_buffer(self, buffer, embed: Embed = None) -> None:
        if embed is None:
            embed = Embed()

        file_name = uuid4()

        embed.set_image(url=f"attachment://{file_name}.png")

        file = File(fp=buffer, filename=f"{file_name}.png")

        await self.send(embed=embed, file=file)
