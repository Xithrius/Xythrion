import asyncio
from io import BytesIO

import numpy as np
from discord import Embed, File
from discord.ext.commands import Cog, Context, command
from PIL import Image

from xythrion.bot import Xythrion
from xythrion.utils import convert_3d_tuples

TUPLE_BOOL_3D = tuple[bool, bool, bool]
TUPLE_INT_3D = tuple[int, int, int]


# https://github.com/nkmk/python-snippets/blob/master/notebook/numpy_generate_gradient_image.py
def get_gradient_2d(
    start: int, stop: int, width: int, height: int, is_horizontal: bool
):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, width), (height, 1))
    else:
        return np.tile(np.linspace(start, stop, height), (width, 1)).T


def get_gradient_3d(
    width: int,
    height: int,
    start_list: TUPLE_INT_3D,
    stop_list: TUPLE_INT_3D,
    is_horizontal_list: TUPLE_BOOL_3D,
):
    result = np.zeros((height, width, len(start_list)))

    for i, (start, stop, is_horizontal) in enumerate(
        zip(start_list, stop_list, is_horizontal_list)
    ):
        result[:, :, i] = get_gradient_2d(
            start, stop, width, height, is_horizontal
        )

    return result


def generate_image(
    start_color: TUPLE_INT_3D,
    end_color: TUPLE_INT_3D,
    size: tuple[int, int],
    gradient_direction: TUPLE_BOOL_3D,
) -> BytesIO:
    array = get_gradient_3d(
        size[0], size[1], start_color, end_color, gradient_direction
    )
    img = Image.fromarray(np.uint8(array)).convert("RGBA")

    buffer = BytesIO()
    img.save(buffer, "png")
    buffer.seek(0)

    return buffer


class GradientImageGenerator(Cog):
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
            lambda: generate_image(
                start, end, (size_h, size_v), gradient_direction
            )
        )

        embed = Embed()

        embed.set_image(url="attachment://tmp_gradient.png")

        file = File(fp=buffer, filename="tmp_gradient.png")

        await ctx.send(embed=embed, file=file)
