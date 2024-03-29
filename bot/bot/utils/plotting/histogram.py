from io import BytesIO

import pandas as pd
import seaborn as sns

from bot.context import Context
from bot.utils import remove_outliers, to_async

from .errors import EmptyFigureError


async def plot_histogram_2d(
    df: pd.DataFrame,
    *,
    title: str = "Value distribution",
    x_label: str = "value",
    y_label: str = "frequency",
    include_outliers: bool = False,
    ctx: Context | None = None,
) -> BytesIO | None:
    @to_async
    def __build_histogram_2d(data: pd.DataFrame) -> BytesIO:
        sns.set_theme()
        svm = sns.histplot(data, kde=True, x=x_label)

        svm.set_title(title)

        svm.set_xlabel(x_label.capitalize())
        svm.set_ylabel(y_label.capitalize())

        buffer = BytesIO()

        if (fig := svm.get_figure()) is None:
            raise EmptyFigureError("Figure of line plot is empty.")

        fig.savefig(buffer, format="png")
        buffer.seek(0)
        fig.clf()

        return buffer

    if not include_outliers:
        df = remove_outliers(df, x_label)

    b = await __build_histogram_2d(df)

    if ctx is None:
        return b

    await ctx.send_image_buffer(b)

    return None
