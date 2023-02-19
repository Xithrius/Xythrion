from io import BytesIO

import numpy as np
from loguru import logger as log

from xythrion.utils import noblock

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.style.use("dark_background")

except (ImportError, ImportWarning) as e:
    log.error("Error when importing Matplotlib.",
              exc_info=(type(e), e, e.__traceback__))


@noblock
async def graph_2d(
    x: np.ndarray,
    y: np.ndarray,
    *,
    plot_type: str = "line",
    autorotate_xaxis: bool = True
) -> BytesIO:
    buffer = BytesIO()
    fig, axis = plt.subplots()

    axis.grid(True, linestyle="-.", linewidth=0.5)

    if plot_type == "bar":
        placements = np.linspace(0, len(x) + 1, len(x))
        axis.bar(placements, y, 0.5)
        axis.set_xticks(placements)
        axis.set_xticklabels(x)
    else:
        axis.plot(x, y)

    if autorotate_xaxis:
        plt.gcf().autofmt_xdate()

    fig.savefig(buffer, format="png")

    buffer.seek(0)

    return buffer

# from io import BytesIO
#
# import matplotlib as plt
# import numpy as np
#
#
# def graph(x: np.ndarray, y: np.ndarray) -> BytesIO:
#     """Plotting pre-calculated x/y points."""
#     buffer = BytesIO()
#     fig, ax = plt.subplots()
#     fig.tight_layout(pad=0.3, w_pad=0.2, h_pad=0.5)
#
#     ax.grid(True, linestyle="-.", linewidth=0.5)
#
#     ax.spines["left"].set_position("zero")
#     ax.spines["right"].set_color("none")
#     ax.spines["bottom"].set_position("zero")
#     ax.spines["top"].set_color("none")
#
#     ax.plot(x, y)
#
#     fig.savefig(buffer, format="png")
#     buffer.seek(0)
#
#     return buffer
