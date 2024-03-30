import pytest

from bot.utils import remove_whitespace, str_to_tuple3


def test_remove_some_whitespace() -> None:
    assert remove_whitespace("t est ") == "test"


def test_remove_no_whitespace() -> None:
    assert remove_whitespace("test") == "test"


def test_convert_single_digits_in_tuple() -> None:
    assert str_to_tuple3("(2,2,2)") == (2, 2, 2)


def test_convert_multiple_digits_in_tuple() -> None:
    assert str_to_tuple3("(12,23,24)") == (12, 23, 24)


def test_convert_different_digits_in_tuple() -> None:
    assert str_to_tuple3("(1,22,333)") == (1, 22, 333)


def test_convert_no_digits_in_tuple() -> None:
    with pytest.raises(ValueError):
        str_to_tuple3("(asdf,asdf,asdf)")
