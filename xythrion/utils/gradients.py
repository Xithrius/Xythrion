import numpy as np


# https://github.com/nkmk/python-snippets/blob/master/notebook/numpy_generate_gradient_image.py
def gradient2(
    start: int, stop: int, width: int, height: int, is_horizontal: bool
):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, width), (height, 1))
    else:
        return np.tile(np.linspace(start, stop, height), (width, 1)).T


def gradient3(
    width: int,
    height: int,
    start_list: tuple[int, int, int],
    stop_list: tuple[int, int, int],
    is_horizontal_list: tuple[bool, bool, bool],
):
    result = np.zeros((height, width, len(start_list)))

    for i, (start, stop, is_horizontal) in enumerate(
        zip(start_list, stop_list, is_horizontal_list)
    ):
        result[:, :, i] = gradient2(start, stop, width, height, is_horizontal)

    return result
