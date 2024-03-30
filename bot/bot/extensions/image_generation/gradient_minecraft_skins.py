import asyncio
from io import BytesIO

import numpy as np
from discord.ext.commands import Cog, command
from PIL import Image

from bot.bot import Xythrion
from bot.context import Context
from bot.utils import gradient3, str_to_tuple3

REMOVE_IMAGE_SECTIONS = [
    (0, 8, 0, 8),
    (0, 8, 24, 64),
    (8, 16, 32, 64),
    (16, 20, 0, 4),
    (16, 20, 12, 20),
    (16, 20, 36, 44),
    (16, 20, 52, 64),
    (32, 64, 0, 16),
    (32, 48, 16, 64),
    (48, 64, 48, 64),
    (48, 52, 44, 48),
    (48, 52, 28, 36),
    (48, 52, 16, 20),
    (20, 32, 56, 64),
]


class GradientMinecraftSkins(Cog):
    """Generating gradient Minecraft skins."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @staticmethod
    def generate_gradient_skin_image(
        start_color: tuple[int, ...],
        end_color: tuple[int, ...],
        gradient_direction: tuple[bool, bool, bool] = (False, False, False),
        size_h: int = 64,
        size_v: int = 64,
    ) -> BytesIO:
        array = gradient3(size_h, size_v, start_color, end_color, gradient_direction)
        img = Image.fromarray(np.uint8(array)).convert("RGBA")

        img_arr = np.array(img)

        img_arr[48:64, 16:32] = np.copy(img_arr[28:44, 16:32])
        img_arr[16:32, 0:16] = np.copy(img_arr[28:44, 16:32])

        for y1, y2, x1, x2 in REMOVE_IMAGE_SECTIONS:
            img_arr[y1:y2, x1:x2] = (0, 0, 0, 0)

        img_arr[48:64, 32:48] = img_arr[16:32, 40:56]

        img = Image.fromarray(img_arr)

        buffer = BytesIO()
        img.save(buffer, "png")
        buffer.seek(0)

        return buffer

    @command()
    async def gradient_skin(
        self,
        ctx: Context,
        start: str,
        end: str,
    ) -> None:
        buffer = await asyncio.to_thread(
            lambda: self.generate_gradient_skin_image(
                str_to_tuple3(start),
                str_to_tuple3(end),
            ),
        )

        await ctx.send_image_buffer(buffer)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(GradientMinecraftSkins(bot))
