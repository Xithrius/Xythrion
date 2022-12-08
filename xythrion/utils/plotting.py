from io import BytesIO

import matplotlib as plt
import numpy as np


def graph(x: np.ndarray, y: np.ndarray) -> BytesIO:
    """Plotting pre-calculated x/y points."""
    buffer = BytesIO()
    fig, ax = plt.subplots()
    fig.tight_layout(pad=0.3, w_pad=0.2, h_pad=0.5)

    ax.grid(True, linestyle="-.", linewidth=0.5)

    ax.spines["left"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_color("none")

    ax.plot(x, y)

    fig.savefig(buffer, format="png")
    buffer.seek(0)

    return buffer
