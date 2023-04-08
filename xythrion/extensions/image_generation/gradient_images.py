import asyncio
from io import BytesIO

import numpy as np
from discord.ext.commands import Cog, command
from PIL import Image

from xythrion.bot import Xythrion
from xythrion.context import Context
from xythrion.utils import convert_3d_tuples, gradient3


def __generate_gradient_image(
    start_color: tuple[int, int, int],
    end_color: tuple[int, int, int],
    size: tuple[int, int],
    gradient_direction: tuple[bool, bool, bool],
) -> BytesIO:
    array = gradient3(
        size[0], size[1], start_color, end_color, gradient_direction
    )
    img = Image.fromarray(np.uint8(array)).convert("RGBA")

    buffer = BytesIO()
    img.save(buffer, "png")
    buffer.seek(0)

    return buffer


class GradientImages(Cog):
    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command()
    async def gradient(
        self,
        ctx: Context,
        start: convert_3d_tuples,
        end: convert_3d_tuples,
        size_h: int,
        size_v: int,
        direction: str = "h",
    ) -> None:
        gradient_direction = (False, False, False)
        if direction == "h":
            gradient_direction = (True, True, True)
        elif direction == "hv":
            gradient_direction = (True, True, False)
        elif direction == "vh":
            gradient_direction = (False, False, True)

        buffer = await asyncio.to_thread(
            lambda: __generate_gradient_image(
                start, end, (size_h, size_v), gradient_direction
            )
        )

        await ctx.send_buffer(buffer)
