from io import BytesIO

import pandas as pd
import seaborn as sns

from bot.context import Context
from bot.utils import remove_outliers, to_async

from .errors import EmptyFigureError


async def plot_line_2d(
    df: pd.DataFrame,
    *,
    title: str = "Line",
    x_label: str = "x",
    y_label: str = "y",
    include_outliers: bool | None = False,
    ctx: Context | None,
) -> BytesIO | None:
    @to_async
    def __build_line_2d(data: pd.DataFrame) -> BytesIO:
        sns.set_theme()
        svm = sns.lineplot(data, x=x_label)

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

    b = await __build_line_2d(df)

    if ctx is None:
        return b

    return await ctx.send_image_buffer(b)
