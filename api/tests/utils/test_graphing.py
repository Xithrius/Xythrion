import pytest

from api.utils.graphing import sanitize_expression


def test_sanitize_expression_empty():
    with pytest.raises(ValueError):
        assert sanitize_expression("")

def test_sanitize_expression_some_valid():
    assert sanitize_expression("x + 2")

def test_sanitize_expression_no_x():
    assert sanitize_expression("2")

def test_sanitize_expression_no_x_some_y():
    assert sanitize_expression("y + 2")
