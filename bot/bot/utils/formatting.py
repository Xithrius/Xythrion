from collections.abc import Sequence
from datetime import UTC, datetime, timezone

import pandas as pd
from humanize import naturaldelta
from tabulate import tabulate  # type: ignore [import-untyped]

FAKE_DISCORD_NEWLINE = "||\n||"


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


def codeblock(code: str | list | dict, *, language: str | None = None) -> str:
    """Returns a string in the format of a Discord codeblock."""
    if isinstance(code, list):
        block = "\n".join(str(x) for x in code)
    else:
        block = str(code)

    return f"```{language or ''}\n{block}\n```"


def convert_to_deltas(
    df: pd.DataFrame,
    *,
    datetime_key: str,
    tz: timezone = UTC,
) -> pd.DataFrame:
    """Converts a datetime in a DataFrame to a human-readable delta."""
    current_time = datetime.now(tz=tz)

    def __datetime_conversion(x: str) -> str:
        created_time = datetime.fromisoformat(str(x).rstrip("Z")).replace(tzinfo=tz)
        delta = created_time - current_time
        return naturaldelta(delta.total_seconds())

    df[datetime_key] = df[datetime_key].apply(__datetime_conversion)

    return df


def dict_to_human_table(
    data: dict,
    *,
    headers: str | dict[str, str] | Sequence[str] = "keys",
) -> str:
    table = tabulate(
        list(data.values()),
        headers=headers,
        maxcolwidths=36,
        stralign="left",
        colalign=["left"] * len(headers),
    )

    return table


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
        return f"{ns / microsecond_threshold:.2f}μs"

    if ns < second_threshold:
        return f"{ns / millisecond_threshold:.2f}ms"

    return f"{ns / second_threshold:.2f}s"
