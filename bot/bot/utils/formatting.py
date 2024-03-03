from datetime import datetime, timedelta, timezone

from humanize import naturaldelta
from tabulate import tabulate


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


def final_join(items: list[str], *, sep: str | None = ", ", final: str | None = "and") -> str:
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
    data: dict,
    *,
    datetime_key: str,
    tz: timezone | None = None,
) -> dict:
    """Converts a datetime in a dictionary to a human-readable delta."""
    current_time = datetime.now(
        tz=tz if tz is not None else timezone(timedelta(hours=0.0)),
    )

    for item in data:
        created_time = datetime.fromisoformat(item[datetime_key].rstrip("Z"))
        delta = created_time - current_time
        item[datetime_key] = naturaldelta(delta.total_seconds())

    return data


def dict_to_human_table(data: dict, *, datetime_key: str | None = None) -> str:
    """Dictionary to readable table."""
    if (key := datetime_key) is not None:
        data = convert_to_deltas(data, datetime_key=key)

    table = tabulate(data, headers="keys")
    block = codeblock(table)

    return block


def format_nanosecond_time(
    ns: int,
    *,
    microsecond_threshold: int | None = 1_000,
    millisecond_threshold: int | None = 1_000_000,
    second_threshold: int | None = 1_000_000_000,
) -> str:
    if ns < microsecond_threshold:
        return f"{ns}ns"

    if ns < millisecond_threshold:
        return f"{ns / microsecond_threshold:.2f}µs"

    if ns < second_threshold:
        return f"{ns / millisecond_threshold:.2f}ms"

    return f"{ns / second_threshold:.2f}s"
