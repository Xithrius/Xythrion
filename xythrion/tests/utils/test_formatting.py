from xythrion.utils import markdown_link, and_join

import pytest

def test_markdown_link_no_desc():
    with pytest.raises(ValueError):
        markdown_link("", "")

def test_markdown_link_default_wrap():
    linked = "[GitHub](https://github.com/)"

    assert markdown_link("GitHub", "https://github.com/") == linked

def test_markdown_link_some_wrap():
    linked = "[`GitHub`](https://github.com/)"

    assert markdown_link("GitHub", "https://github.com/", "`") == linked

def test_and_join_no_items():
    items = []

    assert and_join(items) == ""

def test_and_join_one_item():
    items = ["testing"]

    assert and_join(items) == "testing"

def test_and_join_some_items():
    items = ["something", "another"]

    assert and_join(items) == "something, and another"
