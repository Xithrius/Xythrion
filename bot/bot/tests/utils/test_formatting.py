import pandas as pd
import pytest

from bot.utils import convert_to_deltas, dict_to_human_table, final_join, markdown_link
from bot.utils.formatting import format_nanosecond_time


def test_markdown_link_no_desc() -> None:
    with pytest.raises(ValueError):
        markdown_link(desc="", link="")


def test_markdown_link_default_wrap() -> None:
    linked = "[GitHub](https://github.com/)"

    assert markdown_link(desc="GitHub", link="https://github.com/") == linked


def test_markdown_link_some_wrap() -> None:
    linked = "[`GitHub`](https://github.com/)"

    assert markdown_link(desc="GitHub", link="https://github.com/", desc_wrapper="`") == linked


def test_and_join_no_items() -> None:
    items: list[str] = []

    assert final_join(items) == ""


def test_and_join_one_item() -> None:
    items = ["testing"]

    assert final_join(items) == "testing"


def test_and_join_some_items() -> None:
    items = ["something", "another"]

    assert final_join(items) == "something, and another"


LINK_MAP_DATAFRAME = pd.DataFrame(
    [
        {
            "server_id": 931030564801245214,
            "input_channel_id": 1218759428145283102,
            "output_channel_id": 1175661347728523284,
            "created_at": "2024-03-30T06:00:41.162139",
        },
    ],
)


def test_dict_to_human_readable_some_items_no_datetime_key() -> None:
    df = LINK_MAP_DATAFRAME.T

    table = dict_to_human_table(df)

    original_values = [str(x) for x in next(iter(df.to_dict().values())).values()]

    extracted_table_values = table.split("\n")[3].split()

    assert original_values == extracted_table_values


def test_format_datetimes_in_dataframe() -> None:
    df = LINK_MAP_DATAFRAME

    table = convert_to_deltas(df.copy(), datetime_key="created_at")

    comparison_series = table["created_at"].ne(df["created_at"])

    any_differences = comparison_series.any()

    assert any_differences


def test_format_nanosecond_time_to_nanoseconds() -> None:
    assert format_nanosecond_time(123) == "123ns"


def test_format_nanosecond_time_to_microseconds() -> None:
    assert format_nanosecond_time(1_123) == "1.12µs"


def test_format_nanosecond_time_to_milliseconds() -> None:
    assert format_nanosecond_time(1_123_123) == "1.12ms"


def test_format_nanosecond_time_to_seconds() -> None:
    assert format_nanosecond_time(1_123_123_123) == "1.12s"
