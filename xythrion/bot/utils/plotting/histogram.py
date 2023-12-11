from io import BytesIO

import pandas as pd
import seaborn as sns
from discord.ext.commands import Context

from bot.utils import remove_outliers, send_image_buffer, to_thread


async def plot_histogram_2d(
    df: pd.DataFrame,
    *,
    title: str | None = "Value distribution",
    x_label: str | None = "value",
    y_label: str | None = "frequency",
    include_outliers: bool | None = False,
    ctx: Context | None,
) -> BytesIO | None:
    @to_thread
    async def __build_histogram_2d(data: pd.DataFrame) -> BytesIO:
        sns.set_theme()
        svm = sns.histplot(data, kde=True, x=x_label)

        svm.set_title(title)

        svm.set_xlabel(x_label.capitalize())
        svm.set_ylabel(y_label.capitalize())

        buffer = BytesIO()
        svm.get_figure().savefig(buffer, format="png")
        buffer.seek(0)

        svm.figure.clf()

        return buffer

    if not include_outliers:
        df = remove_outliers(df, x_label)

    b = await __build_histogram_2d(df)

    if ctx is None:
        return b

    return await send_image_buffer(b, ctx=ctx)
