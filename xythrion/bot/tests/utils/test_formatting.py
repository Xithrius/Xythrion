import pytest

from bot.utils import and_join, markdown_link


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
    items = []

    assert and_join(items) == ""


def test_and_join_one_item() -> None:
    items = ["testing"]

    assert and_join(items) == "testing"


def test_and_join_some_items() -> None:
    items = ["something", "another"]

    assert and_join(items) == "something, and another"
