import pytest

from api.utils.parsing import sanitize_expression


def test_sanitize_expression_empty() -> None:
    with pytest.raises(ValueError):
        assert sanitize_expression("")

def test_sanitize_expression_some_valid() -> None:
    assert sanitize_expression("x + 2")

def test_sanitize_expression_no_x() -> None:
    assert sanitize_expression("2")

def test_sanitize_expression_no_x_some_y() -> None:
    assert sanitize_expression("y + 2")
