from io import BytesIO

import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes

from bot.utils import remove_outliers, to_async

from .errors import EmptyFigureError

ALLOWED_PLOT_TYPES = {
    "histogram": lambda df, x_l: sns.histplot(df, kde=True, x=x_l),
    "line": lambda df, x_l: sns.lineplot(df, x=x_l),
    "scatter": lambda df, x_l: sns.scatterplot(df),
}


@to_async
def plot_generic_2d(
    df: pd.DataFrame,
    *,
    plot_type: str,
    title: str = "Plot",
    x_label: str | None = "x",
    y_label: str | None = "y",
    remove_df_outliers: bool = False,
) -> BytesIO:
    """
    Creating a generic type of plot.

    Args:
        df (pd.DataFrame): Data to be plotted.
        plot_type (str): Seaborn plot type (histogram, line, scatter).
        title (str, optional): The title of the plot. Defaults to "Plot".
        x_label (str | None, optional): X axis label. Defaults to "x".
        y_label (str | None, optional): Y axis label. Defaults to "y".
        remove_df_outliers (bool, optional): If scipy should be used to remove x-axis outliers. Defaults to False.

    Raises:
        ValueError: If the inputted plot type does not exist.
        ValueError: If there are no points that were plotted in the figure.

    Returns:
        BytesIO: A byte array representation of the plot image in PNG format.
    """
    if plot_type not in ALLOWED_PLOT_TYPES:
        raise ValueError(f"Plot type of '{plot_type}' does not exist")

    def __build_plot(data: pd.DataFrame) -> BytesIO:
        sns.set_theme()
        plot_func = ALLOWED_PLOT_TYPES[plot_type]
        svm: Axes = plot_func(data, x_l=x_label)

        svm.set_title(title)
        if (x_l := x_label) is not None:
            svm.set_xlabel(x_l.capitalize())
        if (y_l := y_label) is not None:
            svm.set_ylabel(y_l.capitalize())

        buffer = BytesIO()
        if (fig := svm.get_figure()) is None:
            raise EmptyFigureError(f"Figure of {plot_type} plot is empty.")

        fig.savefig(buffer, format="png")
        buffer.seek(0)
        fig.clear()

        return buffer

    if not remove_df_outliers and (x_l := x_label) is not None:
        df = remove_outliers(df, x_l)

    b = __build_plot(df)

    return b
