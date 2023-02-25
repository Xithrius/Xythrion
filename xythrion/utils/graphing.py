from io import BytesIO

import numpy as np
from loguru import logger as log

from xythrion.utils.executor import noblock

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.style.use("dark_background")

except (ImportError, ImportWarning) as e:
    log.error("Error when importing Matplotlib.",
              exc_info=(type(e), e, e.__traceback__))


@noblock
def graph_2d(
    x: np.ndarray,
    y: np.ndarray,
) -> BytesIO:
    buffer = BytesIO()

    fig, axis = plt.subplots()
    axis.grid(True, linestyle="-.", linewidth=0.5)

    axis.plot(x, y)

    fig.savefig(buffer, format="png")

    buffer.seek(0)

    return buffer

# @noblock
# def graph_2d(
#     x: np.ndarray,
#     y: np.ndarray,
#     *,
#     plot_type: str = "line",
#     autorotate_xaxis: bool = True
# ) -> BytesIO:
#     buffer = BytesIO()
#     fig, axis = plt.subplots()
#
#     axis.grid(True, linestyle="-.", linewidth=0.5)
#
#     if plot_type == "bar":
#         placements = np.linspace(0, len(x) + 1, len(x))
#         axis.bar(placements, y, 0.5)
#         axis.set_xticks(placements)
#         axis.set_xticklabels(x)
#     else:
#         axis.plot(x, y)
#
#     # if autorotate_xaxis:
#     #     plt.gcf().autofmt_xdate()
#
#     # axis.spines["left"].set_position("zero")
#     # axis.spines["right"].set_color("none")
#     # axis.spines["bottom"].set_position("zero")
#     # axis.spines["top"].set_color("none")
#
#     fig.savefig(buffer, format="png")
#
#     buffer.seek(0)
#
#     return buffer
