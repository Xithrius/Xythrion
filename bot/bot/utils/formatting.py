from datetime import datetime, timedelta, timezone

import pandas as pd
from humanize import naturaldelta
from tabulate import tabulate  # type: ignore [import-untyped]


def markdown_link(
    *,
    desc: str,
    link: str,
    desc_wrapper: str = "",
) -> str:
    """Gets rid of the thinking while creating a link for markdown."""
    if not (desc or link):
        raise ValueError("Description and link must exist")
    return f"[{desc_wrapper}{desc}{desc_wrapper}]({link})"


def final_join(
    items: list[str],
    *,
    sep: str = ", ",
    final: str = "and",
) -> str:
    """Joins a list by a separator with a final join at the very end."""
    items_length = len(items)

    if items_length <= 1:
        return "" if items_length == 0 else items[0]
    return f"{sep.join(str(x) for x in items[:-1])}{sep}{final} {items[-1]}"


def codeblock(code: str | list[str], *, language: str | None = None) -> str:
    """Returns a string in the format of a Discord codeblock."""
    block = "\n".join(code) if isinstance(code, list) else code

    return f"```{language or ''}\n{block}\n```"


def convert_to_deltas(
    data: pd.DataFrame,
    *,
    datetime_key: str,
    tz: timezone | None = None,
) -> pd.DataFrame:
    """Converts a datetime in a DataFrame to a human-readable delta."""
    current_time = datetime.now(
        tz=tz if tz is not None else timezone(timedelta(hours=0.0)),
    )

    for idx, row in data.iterrows():
        created_time = datetime.fromisoformat(str(row[datetime_key]).rstrip("Z"))
        delta = created_time - current_time
        data.at[idx, datetime_key] = naturaldelta(delta.total_seconds())

    return data


def dict_to_human_table(data: pd.DataFrame, *, datetime_key: str | None = None) -> str:
    """DataFrame to readable table."""
    if datetime_key is not None:
        data = convert_to_deltas(data, datetime_key=datetime_key)

    table = tabulate(list(data.to_dict().values()), headers="keys", tablefmt="grid")
    block = codeblock(table)

    return block


def format_nanosecond_time(
    ns: int,
    *,
    microsecond_threshold: int = 1_000,
    millisecond_threshold: int = 1_000_000,
    second_threshold: int = 1_000_000_000,
) -> str:
    if ns < microsecond_threshold:
        return f"{ns}ns"

    if ns < millisecond_threshold:
        return f"{ns / microsecond_threshold:.2f}µs"

    if ns < second_threshold:
        return f"{ns / millisecond_threshold:.2f}ms"

    return f"{ns / second_threshold:.2f}s"
