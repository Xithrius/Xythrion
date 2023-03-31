import asyncio
from io import BytesIO

import numpy as np
from PIL import Image
from discord import Embed, File
from discord.ext.commands import Cog, Context, command
from loguru import logger as log

from xythrion.bot import Xythrion


# https://github.com/nkmk/python-snippets/blob/master/notebook/numpy_generate_gradient_image.py
def get_gradient_2d(
    start: int,
    stop: int,
    width: int,
    height: int,
    is_horizontal: bool
):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, width), (height, 1))
    else:
        return np.tile(np.linspace(start, stop, height), (width, 1)).T


def get_gradient_3d(
    width: int,
    height: int,
    start_list: tuple[int, int, int],
    stop_list: tuple[int, int, int],
    is_horizontal_list: tuple[bool, bool, bool]
):
    result = np.zeros((height, width, len(start_list)))

    for i, (start, stop, is_horizontal) in enumerate(
        zip(start_list, stop_list, is_horizontal_list)
    ):
        result[:, :, i] = get_gradient_2d(start, stop, width, height, is_horizontal)

    return result


def generate_image() -> BytesIO:
    gradient_direction = (False, False, False)

    start_color = (8, 159, 143)
    end_color = (42, 72, 88)

    array = get_gradient_3d(64, 64, start_color, end_color, gradient_direction)
    img = Image.fromarray(np.uint8(array)).convert('RGBA')

    buffer = BytesIO()
    img.save(buffer, 'png')
    buffer.seek(0)

    return buffer


class GradientImageGenerator(Cog):
    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command()
    async def gradient(self, ctx: Context) -> None:
        log.info('test')

        buffer = await asyncio.to_thread(lambda: generate_image())

        embed = Embed()

        embed.set_image(url="attachment://tmp_gradient.png")

        file = File(fp=buffer, filename="tmp_gradient.png")

        await ctx.send(embed=embed, file=file)
